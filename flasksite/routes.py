import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flasksite import app, db, bcrypt
from flasksite.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flasksite.models import User
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])  # this route can receive GET and POST requests
def register():
    if current_user.is_authenticated:  # if the user is already authenticated
        return redirect(url_for('home'))  # redirect the user to the home page
    form = RegistrationForm()  # instanciates a new form -- lecture 6
    if form.validate_on_submit():  # if the user submitted data and the data is validated
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # create a new instance of the class User -- lecture 6
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)  # adds the user to the database
        try:  # error handling
            # transaction management - databases
            # the changes to the database are only persisted once you commit the session
            db.session.commit()
            app.logger.debug('New user created successfully.')  # error handling
            flash('Your account has been created! You are now able to log in.', 'success')  # show message to user
            return redirect(url_for('login'))
        except Exception as e:
            # transaction management - databases
            # if something goes wrong with the transaction, you need to rollback the session
            db.session.rollback()
            app.logger.critical(f'Error while creating the user {user}')  # error handling
            app.logger.exception(e)  # error handling
            flash('The system encountered a problem while creating your account. Try again later.', 'danger')
    return render_template('register.html',
                           title='Register',
                           form=form)


@app.route("/login", methods=['GET', 'POST'])
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
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html',
                           title='Login',
                           form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_compressed_picture(form_picture):
    """
    Function that gets the file contained in the parameter `form_picture`, compresses it to a 125x125 pixels image,
    and saves it to the `static/profile_pics` folder.
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def save_raw_picture(form_picture):
    """
    Function that gets the file contained in the parameter `form_picture`,
    and saves it to the `static/profile_pics` folder.
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    form_picture.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            # (un)comment the lines below to get the desired effect
            # picture_file = save_compressed_picture(form.picture.data)  # this function saves a compressed picture
            picture_file = save_raw_picture(form.picture.data)  # this function saves the exact file
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        try:
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('account'))
        except Exception as e:
            db.session.rollback()
            app.logger.critical(f'Error while updating your account. {current_user}')
            app.logger.exception(e)
            flash('There was an error while updating your account. Try again later.', 'danger')
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html',
                           title='Account',
                           form=form)


# TODO: create here your routes
