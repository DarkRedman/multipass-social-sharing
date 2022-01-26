import secrets

class DebugConfig(object):
    ENV = 'development'
	BASEURL = 'http://localhost:5000/'
	UPLOAD_FOLDER = '/static/images/'
    SECRET_KEY = 'do-i-really-need-this'
    DATABASE = 'multipass'
    DATABASE_PATH = 'db.sqlite'
    AUTHORIZED_FILES_TYPE = {'png', 'jpg', 'jpeg', 'gif', 'svg'}
    SESSION_COOKIE_NAME = 'userSession'

class ProductionConfig(Config):
    ENV = 'production'
	BASEURL = 'https://multi-pass.org/'
	UPLOAD_FOLDER = '/static/images'
	SECRET_KEY = secrets.token_urlsafe(64)
    DB_HOST = 'my.production.database' # not a docker link
    DATABASE = 'multipass'
    DATABASE_PATH = '/srv/multipass.db'
    AUTHORIZED_FILES_TYPE = {'png', 'jpg', 'jpeg', 'gif', 'svg'}
    SESSION_COOKIE_NAME = 'userSession'