import database
import secrets

from views.home import home_blueprint
from views.login import login_blueprint, logout_blueprint
from views.tasks import tasks_blueprint, basic_task_create_blueprint,\
    basic_task_edit_blueprint, basic_task_delete_blueprint, \
    social_network_task_create_blueprint, social_network_task_edit_blueprint, \
    social_network_task_delete_blueprint
from views.userManagement import user_account_blueprint, user_account_create_blueprint, user_account_edit_blueprint
from flask import Flask


# get HTTPS with Talisman
from flask_talisman import Talisman

app = Flask(__name__, static_folder='static')
app.config.from_object('settings.DebugConfig')

app.register_blueprint(home_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(logout_blueprint)

app.register_blueprint(user_account_blueprint)
app.register_blueprint(user_account_create_blueprint)
app.register_blueprint(user_account_edit_blueprint)

app.register_blueprint(tasks_blueprint)
app.register_blueprint(basic_task_create_blueprint)
app.register_blueprint(basic_task_edit_blueprint)
app.register_blueprint(basic_task_delete_blueprint)
app.register_blueprint(social_network_task_create_blueprint)
app.register_blueprint(social_network_task_edit_blueprint)
app.register_blueprint(social_network_task_delete_blueprint)

talisman = Talisman(app, content_security_policy=[])
# no need to run via talisman, run as usual with app.run

if __name__ == '__main__':
    app.run()
