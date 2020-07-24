from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import flash

from ews_app import login
from ews_app import db
from sqlalchemy.orm import relationship
from sqlalchemy import desc, extract
import datetime
import hashlib
import re

roles = {
    '0': {
        'name': "superadmin",
        'description': "Super Admin"
    },
    '1': {
        'name': "admin",
        'description': "Admin Aplikasi EWS di kantor BBWS Pamali Juana"
    },
    '2': {
        'name': "petugas",
        'description': "Petugas Bendungan"
    },
    '3': {
        'name': "pejabat",
        'description': "Pejabat BBWS Pamali Juana"
    }
}


class BaseLog(db.Model):
    __abstract__ = True
    c_user = db.Column(db.String(30))
    c_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    m_user = db.Column(db.String(30))
    m_date = db.Column(db.DateTime)


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))


class Users(UserMixin, db.Model):
    ''' Role above '''
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128))
    role = db.Column(db.String(1))
    is_active = db.Column(db.Boolean, default=True)
    bendungan_id = db.Column(db.Integer, db.ForeignKey('bendungan.id'), nullable=True)

    alert_logs = relationship('AlertLog', backref='user')

    @property
    def role_name(self):
        return roles[self.role]['name']

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.role_name} - {self.username}>"

    def get_logs(self):
        return AlertLog.query.filter(AlertLog.user_id == self.id).all()


class Bendungan(BaseLog):
    __tablename__ = 'bendungan'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.Text)
    ll = db.Column(db.Text)
    muka_air_min = db.Column(db.Float)
    muka_air_normal = db.Column(db.Float)
    muka_air_max = db.Column(db.Float)
    sedimen = db.Column(db.Float)
    bts_elev_awas = db.Column(db.Float)
    bts_elev_siaga = db.Column(db.Float)
    bts_elev_waspada = db.Column(db.Float)
    lbi = db.Column(db.Float)
    volume = db.Column(db.Float)
    lengkung_kapasitas = db.Column(db.Text)
    elev_puncak = db.Column(db.Float)
    kab = db.Column(db.Text)
    wil_sungai = db.Column(db.String(1))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = relationship('Users', backref='bendungan', foreign_keys=[user_id])


class Alert(BaseLog):
    __tablename__ = 'alerts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    coordinates = db.Column(db.Text)
    is_active = db.Column(db.Boolean)

    alert_logs = relationship('AlertLog', backref='alert')

    def set_coordinates(self, long, lat):
        self.coordinates = f"{lat},{long}"

    def get_logs(self):
        return AlertLog.query.filter(AlertLog.alert_id == self.id).all()


class AlertLog(BaseLog):
    __tablename__ = 'alert_logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    issued_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    alert_id = db.Column(db.Integer, db.ForeignKey('alerts.id'))
