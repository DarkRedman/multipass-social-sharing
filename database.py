import sqlite3
import datetime
from flask import current_app, g

PLACEHOLDER_TASK = {
    'task_id': 0,
    'user_id': None,
    'task_name': 'my placeholder task',
    'date': datetime.datetime.now().replace(second=0, microsecond=0).isoformat(),
    'repetition': 'daily',
    'days': 'MO',
    'months': 'JAN',
    'facebook': {
        'isActive': True,
        'message': 'my message',
        'files': ""
    },
    'instagram': {
        'isActive': True,
        'message': 'my message',
        'files': ""
    },
    'twitter': {
        'isActive': True,
        'message': 'my message',
        'files': ""
    }
}


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE_PATH'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db():
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
        db.commit()


def query_db(query, args=(), one=False, lastrowid=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    if lastrowid:
        return cur.lastrowid
    cur.close()
    get_db().commit()
    return (rv[0] if rv else None) if one else rv