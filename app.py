from flask import Flask

from auth import auth_blueprint
from tasks import tasks_blueprint

# get HTTPS with Talisman
from flask_talisman import Talisman

app = Flask(__name__, static_folder='static')
app.config.from_object('settings.DebugConfig')

app.register_blueprint(auth_blueprint)
app.register_blueprint(tasks_blueprint)

talisman = Talisman(app, content_security_policy=[])
# no need to run via talisman, run as usual with app.run

if __name__ == '__main__':
    app.run()
