from flask import Blueprint, request, render_template, redirect, url_for, jsonify, flash
from flask_login import login_required, current_user
from flask_wtf.csrf import generate_csrf
from sqlalchemy import extract, and_
from psycopg2 import IntegrityError
import datetime
import calendar

from ews_app import db, roles_filter
from ews_app.admin import bp


@bp.route('/users')
@login_required
@roles_filter(roles=['admin'])
def users():
    ''' Index Bendungan '''
    return render_template('admin/users/index.html')


@bp.route('/users/add', methods=['POST'])
@login_required
@roles_filter(roles=['admin'])
def user_add():
    ''' Add New Admin or Pejabat User '''
    return redirect(url_for('admin.users'))


@bp.route('/users/add/petugas', methods=['POST'])
@login_required
@roles_filter(roles=['admin'])
def user_add_petugas():
    ''' Add New Petugas User, bind to bendungan '''
    return redirect(url_for('admin.users'))


@bp.route('/users/<user_id>/password', methods=['POST'])
@login_required
@roles_filter(roles=['admin'])
def user_password():
    ''' Change User Password '''
    return redirect(url_for('admin.users'))


@bp.route('/users/<user_id>/deactivate', methods=['POST'])
@login_required
@roles_filter(roles=['admin'])
def user_deactivate():
    ''' Deactivate User '''
    return redirect(url_for('admin.users'))
