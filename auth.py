import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from multipass.database import query_db

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        error = None

        user_exist = query_db("SELECT * FROM users WHERE email=?", (email,), one=True)

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif user_exist:
            error = 'User {} is already registered.'.format(email)        

        if error is None:
            encrypted_password = generate_password_hash(password)
            query_db("INSERT INTO users(email, password) VALUES(?,?)", (email, encrypted_password))
            return redirect(url_for('auth.login'))

        flash(error)
    return render_template('auth/register.html')


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        error = None
        user = query_db('SELECT * FROM users WHERE email = ?', (email,), one=True)

        if user is None or not check_password_hash(user['password'], password):
            error = 'Incorrect email or password.'
        
        if error is None:
            session.clear()
            session['user_id'] = email
            return redirect(url_for('index'))
        
        flash(error)
    return render_template('auth/login.html')


@auth_blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = query_db('SELECT * FROM users WHERE email = ?', (user_id,), one=True)


@auth_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

# @bp.route('/<username>/account', methods=['GET'])
# def route_to_account(username):
#     email = database.get_user_email(username)
#     return render_template('userAccount.html', baseurl=current_app.config['BASEURL'], username=username, email=email)


# @bp.route('/<username>/edit', methods=['POST'])
# def route_to_edit_account(username):
#     email = request.form["email"]
#     password = request.form["password"]
#     database.update_user(email, password)
#     return render_template('login.html', baseurl=current_app.config['BASEURL'], validation_message="user account edited")