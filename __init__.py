import os

from flask import Flask, render_template


def create_app(test_config=True):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config:
        app.config.from_object('multipass.config.DebugConfig')
    else:
        app.config.from_object('multipass.config.ProductionConfig')

    if app.config['ENV'] == 'development':
        app.instance_path = app.root_path
        app.config['DATABASE_PATH'] = os.path.join(app.instance_path, app.config['DATABASE_PATH'])

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Homepage
    @app.route('/')
    def index():
        return render_template('home.html')

    from . import auth
    app.register_blueprint(auth.auth_blueprint)

    from . import tasks
    app.register_blueprint(tasks.tasks_blueprint)

    return app
