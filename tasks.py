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
    tasks_list = []

    for user_task in user_tasks:
        task_id = user_task['task_id']

        facebook_task = query_db("SELECT * FROM FacebookTask WHERE task_id=?", (task_id,), one=True)
        if facebook_task:
            user_task["facebook"]["isActive"] = True
            user_task["facebook"]["message"] = facebook_task['message']
            user_task["facebook"]["files"] = facebook_task['files']
        
        instagram_task = query_db("SELECT * FROM InstagramTask WHERE task_id=?", (task_id,), one=True)
        if instagram_task:
            user_task["instagram"]["isActive"] = True
            user_task["instagram"]["message"] = instagram_task['message']
            user_task["instagram"]["files"] = instagram_task['files']
        
        twitter_task = query_db("SELECT * FROM TwitterTask WHERE task_id=?", (task_id,), one=True)
        if twitter_task:
            user_task["twitter"]["isActive"] = True
            user_task["twitter"]["message"] = twitter_task['message']
            user_task["twitter"]["files"] = twitter_task['files']

        tasks_list.append(user_task)
    
    # Always put the placeholder task so we can use to add a new task in any case
    tasks_list.append(PLACEHOLDER_TASK)
    
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