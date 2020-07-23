from flask import Blueprint, request, render_template, redirect, url_for, jsonify, flash
from flask_login import login_required, current_user
from flask_wtf.csrf import generate_csrf
from sqlalchemy import extract, and_
from psycopg2 import IntegrityError
import datetime
import calendar

from ews_app import db, roles_filter, petugas_check
from ews_app.admin import bp


@bp.route('/bendungan/operasi')
@login_required
@roles_filter(roles=['admin', 'pejabat'])
def operasi():
    ''' Index alert '''
    return render_template('admin/operasi/index.html',
                            title='Operasi')


@bp.route('/bendungan/<bendungan_id>/operasi')
@login_required
@roles_filter(roles=['admin', 'petugas'])
@petugas_check
def operasi_bendungan(bendungan_id):
    ''' Index alert '''
    return render_template('admin/operasi/bendungan.html',
                            title='Operasi',
                            bendungan_id=bendungan_id)


@bp.route('/bendungan/<bendungan_id>/operasi/chart')
@login_required
@roles_filter(roles=['admin', 'pejabat'])
def operasi_chart(bendungan_id):
    ''' Index alert '''
    return render_template('admin/operasi/index.html', title='Operasi')
