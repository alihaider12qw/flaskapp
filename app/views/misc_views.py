# Copyright 2019 Twin Tech Labs. All rights reserved
from sqlalchemy.exc import IntegrityError
from flask import Blueprint, redirect, render_template, current_app
from flask import request, url_for, flash, send_from_directory, jsonify, render_template_string
# from flask_user import current_user, login_required, roles_accepted

from app import db
import app.models.user_models as models
import uuid
import json
import os
import sys
import datetime

# When using a Flask app factory we must use a blueprint to avoid needing 'app' for '@app.route'
main_blueprint = Blueprint('main', __name__, template_folder='templates')


@main_blueprint.route('/')
def member_page():
    doctors = models.Doctor.query.all()
    print("doctors")
    print(doctors)
    return render_template('pages/global.html', doctors=doctors)


@main_blueprint.route('/doctor_profile/<d_id>')
def doctor_prof(d_id):
    doctor = models.Doctor.query.get(d_id)
    print("doctor")
    print(doctor)
    return render_template('pages/doctor_prof.html', doctor=doctor)


@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = models.User.query.filter_by(
            email=email).filter_by(password=password).first()
        if not user:
            return render_template('pages/login.html', err_msg="User does not exist.")

        return redirect(url_for('main.booking', user_id=user.id))
    else:
        return render_template('pages/login.html')


@main_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            fullname = request.form.get("fullname")
            email = request.form.get("email")
            password = request.form.get("password")
            phone = request.form.get("phone")
            date_of_birth = request.form.get("date_of_birth")
            speciality = request.form.get("speciality")

            user = models.User(fullname=fullname, email=email, password=password,
                               phone=phone, date_of_birth=date_of_birth, speciality=speciality)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('main.booking', user_id=user.id))
        except IntegrityError as err:
            import traceback
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno, err, file=sys.stderr)
            return render_template('pages/signup.html', err_msg="Email already exist.")
        except Exception as err:
            import traceback
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno, err, file=sys.stderr)

            return render_template('pages/signup.html', err_msg="Unexpected error occured.")
    else:
        return render_template('pages/signup.html')


@main_blueprint.route('/booking/<user_id>')
def booking(user_id):
    schedules = models.Schedule.query.filter_by(fk_user=user_id).all()
    print("schedules")
    print(schedules)

    return render_template('pages/booking.html', schedules=schedules, user_id=user_id)
