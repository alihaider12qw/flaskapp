# Copyright 2019 Twin Tech Labs. All rights reserved

from flask import Blueprint, redirect, render_template, current_app
from flask import request, url_for, flash, send_from_directory, jsonify, render_template_string
# from flask_user import current_user, login_required, roles_accepted

from app import db
from app.models.user_models import UserProfileForm, User, UsersRoles
import uuid
import json
import os
import datetime

# When using a Flask app factory we must use a blueprint to avoid needing 'app' for '@app.route'
main_blueprint = Blueprint('main', __name__, template_folder='templates')


@main_blueprint.route('/')
def member_page():
    return render_template('pages/global.html')


@main_blueprint.route('/doctor_profile')
def doctor_prof():
    return render_template('pages/doctor_prof.html')


@main_blueprint.route('/login')
def login():
    return render_template('pages/login.html')


@main_blueprint.route('/signup')
def signup():
    return render_template('pages/signup.html')

@main_blueprint.route('/booking')
def booking():
    return render_template('pages/booking.html')

