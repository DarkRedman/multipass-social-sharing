from flask import current_app, Blueprint, render_template, request, redirect, make_response
import database

login_blueprint = Blueprint('login', __name__,)
logout_blueprint = Blueprint('logout', __name__,)


@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        
        if database.validate_user(email, password):
            return render_template("loginFailed.html")
        else:
            response = make_response(redirect(current_app.config['BASEURL'] + 'dashboard'))
            response.set_cookie('email', email)
            response.set_cookie('userID', current_app.config['SECRET_KEY'] + email) # It's risky to use sole SECRET_KEY as cookie in production
            return response


@logout_blueprint.route('/logout')
def logout():
    # remove cookie session
    response = make_response(redirect(current_app.config['BASEURL']))
    response.set_cookie('email', expires=0)
    response.set_cookie('userID', expires=0)
    return response