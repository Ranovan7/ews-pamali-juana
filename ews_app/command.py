import click
import logging
import requests
import datetime
import os
import json
import daemonocle
import paho.mqtt.subscribe as subscribe
from getpass import getpass

from ews_app import app, db
from ews_app.models import Users

logging.basicConfig(
        filename='/tmp/ewspj_command_log.log',
        level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')


@app.cli.command()
@click.option('-s', '--sampling', default='', help='Awal waktu sampling')
def test_command(sampling):
    print(f"Testing Initiated at {sampling}")


@app.cli.command()
def create_admin():
    username = input("enter username: ")
    password = getpass("enter password: ")

    user = Users(
        username=username,
        role='1'
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    print(f"User {username} as admin created")


@app.cli.command()
def create_db():
    """Creates the db tables."""
    db.create_all()
    print("DB Created")


@app.cli.command()
def drop_db():
    """Drops the db tables."""
    key = input("enter key: ")
    if key == 'ok':
        db.drop_all()
        print("DB Dropped")
    else:
        print("Cancelled")
