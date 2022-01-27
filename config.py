import secrets


class Config(object):
    UPLOAD_FOLDER = 'uploads'
    AUTHORIZED_FILES_TYPE = {'png', 'jpg', 'jpeg', 'gif', 'svg'}
    SESSION_COOKIE_NAME = 'userSession'


class DebugConfig(Config):
    ENV = 'development'
    BASEURL = 'http://localhost:5000/'
    SECRET_KEY = 'do-i-really-need-this'
    DATABASE_PATH = 'multipass.db'


class ProductionConfig(Config):
    ENV = 'production'
    BASEURL = 'https://multi-pass.org/'
    SECRET_KEY = secrets.token_urlsafe(64)
    DATABASE_PATH = '/srv/multipass.db'
    DB_HOST = 'my.production.database' # not a docker link