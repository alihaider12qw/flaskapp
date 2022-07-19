# This file defines command line commands for manage.py
#
# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

import datetime

from flask import current_app
from flask_script import Command

from app import db
from app.models.user_models import *


class InitDbCommand(Command):
    """ Initialize the database."""

    def run(self):
        init_db()


def init_db():
    """ Initialize the database."""
    db.drop_all()
    db.create_all()
    create()


def create():
    # Create all tables
    db.create_all()

    # Adding roles
    doctor = Doctor(name="Dr. John Doe",
                    profession="Heart Surgeon",
                    profile_picture_url="doc5.jpeg",
                    qualification="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
                    charges=700)
    db.session.add(doctor)

    schedule = Schedule("1", "First", "Summary is", "Needs surgery", datetime.datetime.now(
    ), datetime.datetime.now(), True, False, "Busy", 1)
    db.session.add(schedule)

    # Save to DB
    db.session.commit()
