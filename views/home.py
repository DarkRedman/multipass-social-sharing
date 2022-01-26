from flask import current_app, Blueprint, render_template

home_blueprint = Blueprint('home', __name__,)


@home_blueprint.route('/', methods=['GET'])
def route_to_home():
    return render_template('home.html', baseurl=current_app.config['BASEURL'])