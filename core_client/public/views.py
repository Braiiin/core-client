from datetime import datetime
from random import random
import functools
from client import hashing, login_manager
from client.exceptions import LogicException
from client.libs.core import User, Session
from core_client.public.forms import LoginForm, RegisterForm
from flask import Blueprint, render_template, url_for, request, current_app
from flask_login import login_user, redirect as flask_redirect, current_user, \
    logout_user

# setup Blueprint
public = Blueprint('public', __name__)


def redirect(location, **kwargs):
    """assembles kwargs as querystring"""
    kwargs = ['%s=%s' % pair for pair in kwargs.items()]
    location = location + '?' + '&'.join(kwargs)
    return flask_redirect(location)


def anonymous_required(f):
    """Require anonymous - otherwise, redirect to private sphere"""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated():
            return redirect(
                request.args.get('next') or url_for('sphere.home'), access_token=current_user.access_token)
        return f(*args, **kwargs)
    return wrapper


@public.route('/')
def landing():
    """Landing page"""
    return render_template('public/index.html')


@public.route('/login', methods=['POST', 'GET'])
@anonymous_required
def login():
    """Login page"""
    try:
        form = LoginForm(request.form)
        next = request.args.get('next', None)
        user = User(username=form.username.data)
        if request.method == 'POST' and form.validate():
            user.get()
            password = hashing.hash_value(form.password.data, salt=user.salt)
            user.authenticate(password=password, salt=None)
            if user.get_id() and user.is_authenticated() and user.is_active():
                if login_user(user):
                    return redirect(
                        request.form.get('next') or url_for('sphere.home'), access_token=user.access_token)
            message = 'Login failed.'
    except LogicException as e:
        message = str(e)
    return render_template('public/login.html', **locals())


@public.route('/register', methods=['POST', 'GET'])
@anonymous_required
def register():
    """Register page"""
    try:
        form = RegisterForm(request.form)
        next = request.args.get('next', None)
        if request.method == 'POST' and form.validate():
            salt = hashing.hash_value(str(datetime.now()))
            password = hashing.hash_value(form.password.data, salt=salt)
            user = User(
                name=form.name.data,
                email=form.email.data,
                password=password,
                salt=salt,
                username=form.username.data
            ).post().authenticate(password=password, salt=None)
            if login_user(user):
                return redirect(
                    request.form.get('next') or url_for('sphere.home'),
                    access_token=user.access_token)
            else:
                return redirect(url_for('public.login'))
    except LogicException as e:
        message = str(e)
    return render_template('public/register.html', **locals())


@public.route('/mission')
def mission():
    """Mission"""
    return 'coming soon'


@login_manager.user_loader
def load_user(access_token):
    """Loading a user from saved userId"""
    session = Session(access_token=access_token).get()
    user = User(id=session.user, access_token=access_token).get()
    session.user = user
    if user.is_active():
        return user
    else:
        return None


@login_manager.unauthorized_handler
def unauthorized():
    """Where unauthenticated users are sent"""
    return redirect(url_for('public.login'))


@public.route('/logout')
def logout():
    """Logout the user"""
    logout_user()
    return redirect(url_for('public.login'))
