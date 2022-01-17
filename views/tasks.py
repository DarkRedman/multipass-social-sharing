import datetime
import os

from flask import Blueprint, render_template, redirect, request
from werkzeug.utils import secure_filename

import database
import settings

baseURL = settings.BASEURL
upload_folder = settings.UPLOAD_FOLDER
secret = settings.SECRET

tasks_blueprint = Blueprint('user', __name__, )
basic_task_create_blueprint = Blueprint('basic_task_create', __name__, )
basic_task_edit_blueprint = Blueprint('basic_task_edit', __name__, )
basic_task_delete_blueprint = Blueprint('basic_task_delete', __name__, )
social_network_task_create_blueprint = Blueprint('social_network_task_create', __name__, )
social_network_task_edit_blueprint = Blueprint('social_network_task_edit', __name__, )
social_network_task_delete_blueprint = Blueprint('social_network_task_delete', __name__, )

task = {
    "date": datetime.datetime.now().replace(second=0, microsecond=0).isoformat(),
    "imagesList": [],
    "message": "mon message",
    "repetition": {
        "days": "MO,TU,WE,TH, FR, SA, SU",
        "months": "JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC",
        "frequency": "weekly"
    },
    "id": 0,
    "taskname": "mon Premier Post"
}


@tasks_blueprint.route('/dashboard', methods=['GET'])
def route_to_user_tasks():
    if request.cookies.get('userID') == secret:
        email = request.cookies.get('email')
        dict_tasks_summary = database.get_user_tasks(email)
        return render_template(
            'tasks.html',
            baseurl=baseURL,
            email=email,
            dict_tasks_summary=dict_tasks_summary
        )
    else:
        return redirect(baseURL + "login")


@basic_task_edit_blueprint.route('/task/update', methods=['POST'])
def route_edit_task():
    if request.cookies.get('userID') == secret:
        email = request.cookies.get('email')
        my_task = {
            "user_id": request.cookies.get('email'),
            "task_id": request.form["task_id"],
            "task_name": request.form["taskname"],
            "message": request.form["message"],
            "date": request.form["date"],
            "repetition_frequency": request.form["repetition_frequency"],
            "days": request.form["days"],
            "months": request.form["months"],
        }

        social_networks = ["facebook", "twitter", "instagram"]

        for social_network in social_networks:
            if request.form[social_network+"-activated"] == "activated":
                task[social_network] = {"message": request.form[social_network+"-message"]}
                files = request.files.getlist("files[]")

                if len(files) > 1:
                    images_list = []
                    for file in files:
                        file.save(os.path.join(upload_folder, email, secure_filename(file.filename)))
                        images_list.append(secure_filename(file.filename))
                    my_task[social_network+"_files"] = images_list
                if len(files) <= 1:
                    my_task[social_network+"_files"] = []

        database.update_task(email, my_task)
        return redirect("/dashboard")
    else:
        return redirect(baseURL)


@basic_task_delete_blueprint.route('/task/delete', methods=['POST'])
def route_to_delete_task():
    if request.cookies.get('userID') == secret:
        database.delete_basic_task(
            request.cookies.get('email'),
            request.form['task_id'],
        )
        return redirect("/dashboard")
    else:
        return redirect(baseURL)
