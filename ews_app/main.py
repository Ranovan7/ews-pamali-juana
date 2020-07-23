import datetime
from flask import render_template, redirect, url_for, flash, request, abort, Blueprint
from flask_login import current_user, login_required, login_user, logout_user

from ews_app import app
from ews_app.models import Users
from ews_app.forms import LoginForm

bp = Blueprint('', __name__)


@app.context_processor
def always_on():
    return dict(user=current_user)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('master/404.html'), 404


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if not user.check_password(form.password.data):
                # print(f"wrong password : {form.password.data}")
                flash('Password keliru', 'danger')
                return redirect(url_for('login'))
            login_user(user)
            dest_url = request.args.get('next')
            if not dest_url:
                dest_url = url_for("admin.dashboard")
            flash('Login Sukses', 'success')
            return redirect(dest_url)
        else:
            # print("not Found")
            flash('User tidak ditemukan', 'danger')
            return redirect(url_for('login'))
    return render_template('auth/login.html', title='Login', form=form)


@app.route('/')
def index():
    ''' Index EWS '''
    return render_template('main/index.html', title='Info')
