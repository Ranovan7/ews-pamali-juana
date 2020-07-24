import datetime
from flask import render_template, redirect, url_for, flash, request, abort, Blueprint
from flask_login import current_user, login_required, login_user, logout_user

from ews_app import app, roles_filter

bp = Blueprint('admin', __name__)


@bp.route('/')
@login_required
@roles_filter(roles=['admin', 'pejabat'])
def dashboard():
    ''' Dashboard EWS '''
    print("dashboard")
    return render_template('admin/dashboard.html')


import ews_app.admin.alert
import ews_app.admin.bendungan
import ews_app.admin.operasi
import ews_app.admin.users
