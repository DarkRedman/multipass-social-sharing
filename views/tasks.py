import os

from flask import current_app, Blueprint, render_template, redirect, request
from werkzeug.utils import secure_filename

import database

tasks_blueprint = Blueprint('user', __name__, )
basic_task_create_blueprint = Blueprint('basic_task_create', __name__, )
basic_task_edit_blueprint = Blueprint('basic_task_edit', __name__, )
basic_task_delete_blueprint = Blueprint('basic_task_delete', __name__, )
social_network_task_create_blueprint = Blueprint('social_network_task_create', __name__, )
social_network_task_edit_blueprint = Blueprint('social_network_task_edit', __name__, )
social_network_task_delete_blueprint = Blueprint('social_network_task_delete', __name__, )


@tasks_blueprint.route('/dashboard', methods=['GET'])
def route_to_user_tasks():
    if request.cookies.get('userID') == current_app.config['SECRET_KEY']:
        email = request.cookies.get('email')
        tasks_list = database.get_user_tasks(email)
        return render_template(
            'tasks.html',
            baseurl=current_app.config['BASEURL'],
            email=email,
            tasks_list=tasks_list
        )
    else:
        return redirect(current_app.config['BASEURL'] + "login")


@basic_task_edit_blueprint.route('/task/update', methods=['POST'])
def route_edit_task():
    if request.cookies.get('userID') == current_app.config['SECRET_KEY']:
        email = request.cookies.get('email')
        my_task = {
            "user_id": email,
            "task_id": request.form["id"],
            "task_name": request.form["taskname"],
            "date": request.form["date"],
            "repetition_frequency": request.form["repetition_frequency"],
            "days": request.form["days"],
            "months": request.form["months"],
        }
        social_networks = ["facebook", "twitter", "instagram"]

        for social_network in social_networks:
            current_app.logger.info(social_network+"-activated")
            if request.form[social_network+"-activated"] == "True":
                files = request.files.getlist("files[]")
                image_list_string = ""

                if len(files) > 1:
                    images_list = []
                    for file in files:
                        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], email, secure_filename(file.filename)))
                        images_list.append(secure_filename(file.filename))
                    image_list_string = str(images_list)
                my_task[social_network] = {
                    social_network+"-message": request.form[social_network+"-message"],
                    social_network+"-files": image_list_string
                }
        database.update_task(my_task["task_id"], my_task["user_id"], my_task["task_name"], my_task["date"], my_task["repetition_frequency"], my_task["days"], my_task["months"])
        return redirect("/dashboard")
    else:
        return redirect(current_app.config['BASEURL'])


@basic_task_delete_blueprint.route('/task/delete', methods=['POST'])
def route_to_delete_task():
    if request.cookies.get('userID') == current_app.config['SECRET_KEY']:
        database.delete_basic_task(
            request.cookies.get('email'),
            request.form['task_id'],
        )
        return redirect("/dashboard")
    else:
        return redirect(current_app.config['BASEURL'])
