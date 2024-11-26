from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import or_
from app.home import blueprint
from app import db, login_manager
from flask import flash, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm, RegistrationForm
from app.models import Users


@blueprint.route('/')
def index():
    return redirect(url_for('home_blueprint.login'))

@blueprint.route('/home')
@login_required
def home():
    return render_template('home/home.html', segment='Dashboard')


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('home_blueprint.home'))
        else:
            flash('Invalid username or password', 'error')
    if not current_user.is_authenticated:
        return render_template('home/login.html',
                               form=form, segment="login")
    return redirect(url_for('home_blueprint.home'))

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if not current_user.is_authenticated:
        if form.validate_on_submit():
            # Check if the email or username already exists
            existing_user = Users.query.filter(or_(Users.username == form.username.data)).first()
            if existing_user:
                flash('Registration failed. Email or username already exists.', 'danger')
                return redirect(url_for('home_blueprint.register'))
            
            # Create a new user
            user = Users(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('home_blueprint.login'))
        
        return render_template('home/register.html', title='Register', form=form, segment="register")
    return redirect(url_for('home_blueprint.home'))


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_blueprint.login'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    flash('To access that page you need to login first', 'danger')
    return redirect(url_for('home_blueprint.login'))
