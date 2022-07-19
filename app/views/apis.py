# Copyright 2019 Twin Tech Labs. All rights reserved

from flask import Blueprint, redirect, render_template
from flask import request, url_for, flash, send_from_directory, jsonify, render_template_string
# from flask_user import current_user, login_required, roles_accepted

from app import db
import app.models.user_models as models
import uuid
import json
import os
import datetime
import pytz

# When using a Flask app factory we must use a blueprint to avoid needing 'app' for '@app.route'
api_blueprint = Blueprint('api', __name__, template_folder='templates')


@api_blueprint.route('/sample_call', methods=['GET'])
def sample_page():

    ret = {"sample return": 10}
    return(jsonify(ret), 200)


@api_blueprint.route('/update_schedule/<s_id>', methods=['POST'])
def update_schedule(s_id):
    # return(jsonify({"Error":"err"}), 400) # show error test
    schedules = models.Schedule.query.get(s_id)
    if not schedules:
        return(jsonify({"result": "Error"}), 404)
    post_data = json.loads(request.get_data())
    print("post_data")
    print(post_data)
    # {'title': 'First2', 'location': 'Summary2 is', 'dnotes': 'Needs surgeryss2', 'start': {'_date': '2022-07-20T07:00:00.000Z'}, 'end': {'_date': '2022-07-21T19:00:00.000Z'}, 'isAllDay': False, 'state': 'Free'}

    title = post_data.get("title", None)
    location = post_data.get("location", None)
    dnotes = post_data.get("dnotes", None)
    start = post_data.get("start", None)
    end = post_data.get("end", None)
    isAllDay = post_data.get("isAllDay", None)
    state = post_data.get("state", None)
    isPrivate = post_data.get("isPrivate", None)

    if title is not None:
        schedules.title = title
    if location is not None:
        schedules.location = location
    if dnotes is not None:
        schedules.dnotes = dnotes
    if start is not None:
        schedules.start = datetime.datetime.strptime(
            start['_date'], '%Y-%m-%dT%H:%M:%S.%f%z').astimezone(pytz.timezone('Asia/Karachi'))
    if end is not None:
        schedules.end = datetime.datetime.strptime(
            end['_date'], '%Y-%m-%dT%H:%M:%S.%f%z').astimezone(pytz.timezone('Asia/Karachi'))
    if isAllDay is not None:
        schedules.isAllDay = isAllDay
    if state is not None:
        schedules.state = state
    if isPrivate is not None:
        schedules.isPrivate = isPrivate

    db.session.commit()

    ret = {"sample return": 10}
    return(jsonify(ret), 200)


@api_blueprint.route('/create_schedule', methods=['POST'])
def create_schedule():
    post_data = json.loads(request.get_data())
    print("post_data")
    print(post_data)

    title = post_data.get("title", None)
    calendarId = post_data.get("calendarId", None)
    dnotes = post_data.get("dnotes", None)
    # print(datetime.strptime(post_data.get("end", None)['_date'], '%Y-%m-%dT%H:%M:%S.%f%z'))

    end = datetime.datetime.strptime(
        post_data.get("end", None)['_date'], '%Y-%m-%dT%H:%M:%S.%f%z').astimezone(pytz.timezone('Asia/Karachi'))
    start = datetime.datetime.strptime(
        post_data.get("start", None)['_date'], '%Y-%m-%dT%H:%M:%S.%f%z').astimezone(pytz.timezone('Asia/Karachi'))
    isAllDay = post_data.get("isAllDay", None)
    isPrivate = post_data.get("isPrivate", None)
    location = post_data.get("location", None)
    state = post_data.get("state", None)
    user_id = post_data.get("user_id", None)
    # id= post_data.get("id", None)
    # bgColor= post_data.get("bgColor", None)
    # borderColor= post_data.get("borderColor", None)
    # category= post_data.get("category", None)
    # color= post_data.get("color", None)
    # dragBgColor= post_data.get("dragBgColor", None)
    # dueDateClass= post_data.get("dueDateClass", None)

    schedule = models.Schedule(calendarId=calendarId, title=title, location=location, dnotes=dnotes,
                               end=end, start=start, isAllDay=isAllDay, isPrivate=isPrivate, state=state, fk_user=user_id)
    db.session.add(schedule)
    db.session.commit()

    return(jsonify({"status": "success"}), 200)


@api_blueprint.route('/delete_schedule/<s_id>', methods=['POST'])
def delete_schedule(s_id):
    models.Schedule.query.filter_by(id=s_id).delete()
    db.session.commit()
    return(jsonify({"status": "success"}), 200)
