import secrets
from PIL import Image
import os 
from flask import render_template,url_for, flash, redirect, request
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog import app, db, bcrypt
from flaskblog.models import User,Post
from flask_login import login_user, current_user, logout_user, login_required



posts = [
        {
            'author' : 'Dinesh K',
            'title' : 'Blog post 1',
            'content' : '''Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
        quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
        consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
        cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
        proident, sunt in culpa qui officia deserunt mollit anim id est laborum.''',
            'date_posted' : 'August 18 2021'
        },
        {
            'author' : 'Kanagaraj',
            'title' : 'Blog post 2',
            'content' : '''Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
        quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
        consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
        cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
        proident, sunt in culpa qui officia deserunt mollit anim id est laborum.''',
            'date_posted' : 'August 18 2021'
        }
    ]

@app.route('/') #homepage
@app.route('/home') #multiple routes using the same function
def home():
    return render_template('home.html', posts=posts) #lhs - name of data passed to template



@app.route('/about') #homepage
def about():
    return render_template('about.html', title='About')
    if __name__ == '__main__':
        app.run(debug=True)   #to run via python

@app.route('/register', methods=['GET', 'POST']) #homepage
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You will now be able to log in :)', 'success') #1 time alert
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST']) #homepage
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))  
        else:      
            flash('Login Unsuccessful, please check your email and password!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')   
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
   random_hex = secrets.token_hex(8)
   _, f_ext = os.path.splitext(form_picture.filename) 
   picture_fn = random_hex + f_ext
   picture_path = os.path.join(app.root_path, 'static/Profile_pictures',picture_fn)
   
   output_size=(125,125)
   i = Image.open(form_picture)
   i.thumbnail(output_size)
   i.save(picture_path)
   return picture_fn



@app.route('/account',  methods=['GET', 'POST']) 
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your accont was successfully updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='Profile_pictures/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)