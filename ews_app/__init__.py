import os
import logging
from functools import wraps
from flask import Flask, redirect, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_login import LoginManager, current_user

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
socketio = SocketIO(app)

db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'


# MIDDLEWARES
def roles_filter(roles, *args, **kwargs):
    '''
    Middleware to check roles permission to access an endpoint
    :params roles (list of allowed roles)
    :return
    '''
    def roles_filter_inner(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            role = current_user.role_name
            print(role, roles)
            if role != 'superadmin' and role not in roles:
                return render_template('master/301.html'), 301
            return f(*args, **kwargs)
        return decorated_function
    return roles_filter_inner


def petugas_check(f):
    '''
    Check if user petugas is authorized in this page
    '''
    @wraps(f)
    def decorated_function(bendungan_id, *args, **kwargs):
        if current_user.role_name == 'petugas' and current_user.bendungan_id != int(bendungan_id):
            return render_template('master/forbidden.html'), 301

        return f(bendungan_id, *args, **kwargs)
    return decorated_function


from ews_app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')
from ews_app.main import bp as main_bp
app.register_blueprint(main_bp, url_prefix='')
from ews_app.admin import bp as admin_bp
app.register_blueprint(admin_bp, url_prefix='/admin')

from ews_app import main, models, command

if __name__ == '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    socketio.run(app)
