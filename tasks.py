from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from multipass.auth import login_required
from multipass.db import query_db, PLACEHOLDER_TASK
from .social_networks.twitter import Twitter
import hashlib, os

def hash(email):
    h = hashlib.md5(email.encode())
    return h.hexdigest()

bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@bp.route('/')
@login_required
def index():
    user_tasks = query_db("SELECT * FROM basicTask WHERE user_id=?", (g.user['email'],))
    tasks_list = []

    for user_task in user_tasks:
        user_task = dict(user_task)
        task_id = user_task['task_id']

        facebook_task = query_db("SELECT * FROM FacebookTask WHERE task_id=?", (task_id,), one=True)
        if facebook_task:
            user_task["facebook"] = {}
            user_task["facebook"]["isActive"] = True
            user_task["facebook"]["message"] = facebook_task['message']
            user_task["facebook"]["files"] = facebook_task['files']
        
        instagram_task = query_db("SELECT * FROM InstagramTask WHERE task_id=?", (task_id,), one=True)
        if instagram_task:
            user_task["instagram"] = {}
            user_task["instagram"]["isActive"] = True
            user_task["instagram"]["message"] = instagram_task['message']
            user_task["instagram"]["files"] = instagram_task['files']
        
        twitter_task = query_db("SELECT * FROM TwitterTask WHERE task_id=?", (task_id,), one=True)
        if twitter_task:
            user_task["twitter"] = {}
            user_task["twitter"]["isActive"] = True
            user_task["twitter"]["message"] = twitter_task['message']
            user_task["twitter"]["files"] = twitter_task['files']

        tasks_list.append(user_task)
    
    # Always put the placeholder task so we can use to add a new task in any case
    if tasks_list == []:
        tasks_list.append(PLACEHOLDER_TASK)
    
    return render_template('tasks.html', tasks_list=tasks_list)

@bp.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    email = g.user['email']
    task = query_db("SELECT * FROM basicTask WHERE task_id=? AND user_id=?", (request.form["task_id"], email), one=True)
    is_new = False

    placeholder_task = {
        "user_id": email,
        "task_name": request.form["task_name"],
        "date": request.form["date"],
        "repetition": request.form["repetition"],
        "days": request.form["days"],
        "months": request.form["months"],
    }

    if task is None:
        task = placeholder_task
        # Create new task
        task["task_id"] = query_db("INSERT INTO basicTask(user_id, name, date, repetition, days, months) VALUES(?,?,?,?,?,?)", (task['user_id'], task['task_name'], task['date'], task['repetition'], task['days'], task['months']), lastrowid=True)
        is_new = True
    else:
        task = placeholder_task
        # Update existing task
        task["task_id"] = request.form["task_id"]
        query_db("UPDATE basicTask SET name = ?, date = ?, repetition = ?, days= ?, months=? WHERE task_id = ?", (task['task_name'], task['date'], task['repetition'], task['days'], task['months'], task['task_id']))

    # Update subtasks
    # TODO: detect social_networks from its classes folder, push it to app.config on initialization
    social_networks = ["facebook", "twitter", "instagram"]

    for social_network in social_networks:
        if request.form[social_network+"-activated"] == "True":
            files = request.files
            images_list = []

            for file in files.getlist(f"{social_network}-files-{task['task_id']}"):
                file.save(os.path.join(current_app.instance_path, current_app.config['UPLOAD_FOLDER'], f"{hash(email)}_{secure_filename(file.filename)}"))
                images_list.append(f"{hash(email)}_{secure_filename(file.filename)}")

            if is_new:
                query_db(f"INSERT INTO {social_network.capitalize()}Task(task_id, message, files) VALUES(?,?,?)", (task['task_id'], request.form[social_network+"-message"], ",".join(images_list)))
            else:
                query_db(f"UPDATE {social_network.capitalize()}Task SET message = ?, files = ? WHERE task_id = ?", (request.form[social_network+"-message"], ",".join(images_list), task["task_id"]))
    return redirect(url_for("tasks.index"))

@bp.route('/delete', methods=['POST'])
@login_required
def route_to_delete_task():
    task_id = request.form["task_id"]
    flash(task_id)
    for social_network in ["facebook", "twitter", "instagram"]:
        flash(social_network.capitalize() + "Task")
        query_db(f"DELETE FROM {social_network.capitalize()}Task WHERE task_id=?", (task_id, ))
    query_db("DELETE FROM basicTask WHERE task_id=?", (task_id, ))
    flash("Task deleted")
    return redirect(url_for("tasks.index"))

# TODO: test to integrate in scheduler
@bp.route('/twitter')
@login_required
def twitter():
    try:
        config = {
            'CONSUMER_KEY': current_app.config['CONSUMER_KEY'],
            'CONSUMER_SECRET': current_app.config['CONSUMER_SECRET'],
            'ACCESSTOKEN': current_app.config['ACCESSTOKEN'],
            'ACCESSTOKEN_SECRET': current_app.config['ACCESSTOKEN_SECRET'],
            'UPLOAD_FOLDER': current_app.config['UPLOAD_FOLDER']
        }
    except KeyError:
        config = {}

    tw = Twitter(config)
    if tw.active:
        (f"Successfully logged in Twitter as {tw.logged_as}", "info")
    user_tasks = query_db("SELECT * FROM basicTask WHERE user_id=?", (g.user['email'],))

    
    for user_task in user_tasks:
        twitter_task = query_db("SELECT * FROM TwitterTask WHERE task_id=?", (user_task['task_id'],), one=True)
        files = str(twitter_task['files'])
        files = files.split(",")
        files = [os.path.join(current_app.instance_path, current_app.config['UPLOAD_FOLDER'], secure_filename(file)) for file in files]
        if twitter_task:
            result = tw.share(twitter_task['message'], files)
            if result is False:
                flash('API not configured', 'error')
    return redirect(url_for('tasks.index'))