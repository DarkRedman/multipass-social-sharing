import datetime
from passlib.hash import sha256_crypt
import sqlite3
from flask import current_app
from multipass.social_networks import db_management
from multipass.db import query_db


# ------------------ Users ----------------- #

def get_user_password(email):
    user = query_db("SELECT * FROM users WHERE email=?", (email,), one=True)
    if user:
        return user[1]

def validate_user(email, password):
    if user_exist(email):
        password_query = get_user_password(email)
        if password_query and sha256_crypt.verify(password, password_query):
            return True
    return False

def create_user(email, password):
    encrypted_password = sha256_crypt.hash(password)
    query_db("INSERT INTO users(email, password) VALUES(?,?)", (email, encrypted_password))

def update_user(email, password):
    query_db("UPDATE users SET password = ? WHERE email = ?", (password, email))

def delete_user(email):
    query_db("DELETE FROM users WHERE email = ?", (email,))

def user_exist(email):
    user = query_db("SELECT * FROM users WHERE email=?", (email,), one=True)
    return bool(user)


# ------------------ Tasks ----------------- #

PLACEHOLDER_TASK = {
    'task_id': 0,
    'user_id': None,
    'task_name': 'my task',
    'date': datetime.datetime.now().replace(second=0, microsecond=0).isoformat(),
    'repetition': 'daily',
    'days': 'MO',
    'months': 'JAN',
    'facebook': {
        'isActive': False,
        'message': 'my message',
        'files': ""
    },
    'instagram': {
        'isActive': False,
        'message': 'my message',
        'files': ""
    },
    'twitter': {
        'isActive': False,
        'message': 'my message',
        'files': ""
    }
}

def basic_task_exist(task_id):
    basic_task = query_db("SELECT * FROM basicTask WHERE task_id=?", (task_id,), one=True)
    return bool(basic_task)

def get_facebook_task(task_id):
    return query_db("SELECT * FROM FacebookTask WHERE task_id=?", (task_id,), one=True)

def get_instagram_task(task_id):
    return query_db("SELECT * FROM InstagramTask WHERE task_id=?", (task_id,), one=True)

def get_twitter_task(task_id):
    return query_db("SELECT * FROM TwitterTask WHERE task_id=?", (task_id,), one=True)

def get_user_tasks(email):
    current_app.logger.debug(f"Get tasks for user {email}")
    current_app.logger.debug(user_tasks)
    user_tasks = query_db("SELECT * FROM basicTask WHERE user_id=?", (email,))
    tasks_list = []

    if len(user_tasks) == 0:
        tasks_list.append(PLACEHOLDER_TASK)
    else:
        for user_task in user_tasks:
            task["task_id"] = user_task[0]
            task["user_id"] = user_task[1]
            task["name"] = user_task[2]
            task["date"] = user_task[3]
            task["repetition"] = user_task[4]
            task["days"] = user_task[5]
            task["months"] = user_task[6]

            facebook_task = get_facebook_task(task_id)
            if facebook_task:
                task["facebook"]["isActive"] = True
                task["facebook"]["message"] = facebook_message
                task["facebook"]["files"] = facebook_files
            twitter_task = get_twitter_task(task_id)
            if twitter_task:
                task["twitter"]["isActive"] = True
                task["twitter"]["message"] = twitter_message
                task["twitter"]["files"] = twitter_files
            instagram_task = get_instagram_task(task_id)
            if instagram_task:
                task["instagram"]["isActive"] = True
                task["instagram"]["message"] = instagram_message
                task["instagram"]["files"] = instagram_files
            tasks_list.append(task)
    return tasks_list


def create_task(task_id, user_id, name, date, repetition, days, months):
    sql = ''' INSERT INTO basicTask(task_id, user_id, name, date, repetition, days, months) VALUES(?,?,?,?,?,?,?) '''
    task = (task_id, user_id, name, date, repetition, days, months)

    cursor = connection.cursor()
    cursor.execute(sql, task)
    connection.commit()

    # if "facebook" in task:
    #     create_facebook_task(
    #         task["task_id"],
    #         task.facebook["facebook-message"],
    #         task.facebook["facebook-files"]
    #     )
    # if "twitter" in task:
    #     create_twitter_task(
    #         task["task_id"],
    #         task.twitter["twitter-message"],
    #         task.twitter["twitter-files"]
    #     )
    # if "instagram" in task:
    #     create_instagram_task(
    #         task["task_id"],
    #         task["instagram"]["instagram-message"],
    #         task["instagram"]["instagram-files"]
    #     )


def update_task(task_id, user_id, name, date, repetition, days, months):
    if basic_task_exist(task_id):
        current_app.logger.debug(f"Update task {task_id} for user {user_id} named {name}")
        query_db("UPDATE basicTask SET name = ?, date = ?, repetition = ?, days= ?, months=? WHERE task_id = ?", (name, date, repetition, days, months, task_id))

        # if task["facebook"]:
        #     FacebookTask.update_facebook_task(
        #         task["task_id"],
        #         task.facebook["facebook-message"],
        #         task.facebook["facebook-files"]
        #     )
        # if task["twitter"]:
        #     TwitterTask.update_twitter_task(
        #         task["task_id"],
        #         task.twitter["twitter-message"],
        #         task.twitter["twitter-files"]
        #     )
        # if task["instagram"]:
        #     InstagramTask.update_instagram_task(
        #         task["task_id"],
        #         task.instagram["instagram-message"],
        #         task.instagram["instagram-files"]
        #     )


def delete_basic_task(task_id):
    sql = 'DELETE FROM basicTask WHERE task_id=?'
    cur = conn.cursor()
    cur.execute(sql, (task_id,))
    conn.commit()

    # if FacebookTask.facebook_task_exist(task_id):
    #     FacebookTask.delete_facebook_task(task_id)
    # if TwitterTask.twitter_task_exist(task_id):
    #     TwitterTask.delete_twitter_task(task_id)
    # if InstagramTask.instagram_task_exist(task_id):
    #     InstagramTask.delete_instagram_task(task_id)


def get_max_task_id():
    return BasicTask.get_max_task_id()


def get_frequency_sorted_tasks(frequency, tasks):
    raise NotImplementedError("Not implemented yet")


def get_today_daily_tasks(current_date):
    raise NotImplementedError("Not implemented yet")


def get_today_weekly_tasks(current_date, current_day):
    raise NotImplementedError("Not implemented yet")


def get_today_monthly_tasks(current_date, current_day_int, current_month):
    raise NotImplementedError("Not implemented yet")


def get_today_custom_tasks(current_date, current_day, current_month):
    raise NotImplementedError("Not implemented yet")

# --------------- log activity -------------- #

# def log_task_resume(user_id, task_id, status):
#     db.log.insert_one({"user_id": user_id, "task_id": task_id, "status": status})

