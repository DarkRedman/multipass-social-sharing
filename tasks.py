from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from multipass.auth import login_required
from multipass.db import query_db, PLACEHOLDER_TASK

bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@bp.route('/')
@login_required
def index():
    user_tasks = query_db("SELECT * FROM basicTask WHERE user_id=?", (g.user['email'],))
    tasks_list = user_tasks or [PLACEHOLDER_TASK]
    # for user_task in user_tasks:
    #         task["task_id"] = user_task[0]
    #         task["user_id"] = user_task[1]
    #         task["name"] = user_task[2]
    #         task["date"] = user_task[3]
    #         task["repetition"] = user_task[4]
    #         task["days"] = user_task[5]
    #         task["months"] = user_task[6]

    #         facebook_task = get_facebook_task(task_id)
    #         if facebook_task:
    #             task["facebook"]["isActive"] = True
    #             task["facebook"]["message"] = facebook_message
    #             task["facebook"]["files"] = facebook_files
    #         twitter_task = get_twitter_task(task_id)
    #         if twitter_task:
    #             task["twitter"]["isActive"] = True
    #             task["twitter"]["message"] = twitter_message
    #             task["twitter"]["files"] = twitter_files
    #         instagram_task = get_instagram_task(task_id)
    #         if instagram_task:
    #             task["instagram"]["isActive"] = True
    #             task["instagram"]["message"] = instagram_message
    #             task["instagram"]["files"] = instagram_files
    #         tasks_list.append(task)
    flash(g.user['email'])
    flash(f"user_tasks: {user_tasks}")
    return render_template('tasks.html', tasks_list=tasks_list)

@bp.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    email = g.user['email']

    task = query_db("SELECT * FROM basicTask WHERE task_id=? AND user_id=?", (request.form["id"], email), one=True)
    flash(request.form["taskname"])

    if task is None:
        # Create new task
        task = {
            "user_id": email,
            # "task_id": request.form["id"],
            "task_name": request.form["taskname"],
            "date": request.form["date"],
            "repetition_frequency": request.form["repetition_frequency"],
            "days": request.form["days"],
            "months": request.form["months"],
        }
        flash(f"task_name: {task['task_name']}")
        query_db("INSERT INTO basicTask(user_id, name, date, repetition, days, months) VALUES(?,?,?,?,?,?)", (task['user_id'], task['task_name'], task['date'], task['repetition_frequency'], task['days'], task['months']))
        flash("Task created")
    else:
        # Update existing task
        flash("Task updated")

    # social_networks = ["facebook", "twitter", "instagram"]

    # for social_network in social_networks:
    #     current_app.logger.info(social_network+"-activated")
    #     if request.form[social_network+"-activated"] == "True":
    #         files = request.files.getlist("files[]")
    #         image_list_string = ""

    #         if len(files) > 1:
    #             images_list = []
    #             for file in files:
    #                 file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], email, secure_filename(file.filename)))
    #                 images_list.append(secure_filename(file.filename))
    #             image_list_string = str(images_list)
    #         my_task[social_network] = {
    #             social_network+"-message": request.form[social_network+"-message"],
    #             social_network+"-files": image_list_string
    #         }
    return redirect(url_for("tasks.index"))