# Copyright 2019 Twin Tech Labs. All rights reserved

from flask import Blueprint, redirect, render_template, send_file
from flask import request, url_for, flash, send_from_directory, jsonify, render_template_string
# from flask_user import current_user, login_required, roles_accepted

from app import db
import app.models.user_models as models
import uuid
import json
import os
import sys
import datetime
import pytz
import pdfkit
import codecs
import bs4

# When using a Flask app factory we must use a blueprint to avoid needing 'app' for '@app.route'
api_blueprint = Blueprint('api', __name__, template_folder='templates')
invoice_html = "invoice_send.html"
test = "test.html"

#region helper functions


def generate_pdf_from_html(html_type, filename, html):
    try:
        if html_type == models.HtmlType.File.value:
            pdf_name = "app/static/htmls/"+filename[:-4]+'pdf'
            pdfkit.from_file("app/static/htmls/"+filename, pdf_name)
            return pdf_name

        elif html_type == models.HtmlType.String.value:
            pdf_name = "app/static/htmls/"+filename[:-4]+'pdf'
            pdfkit.from_string(html, pdf_name)
            return pdf_name

    except Exception as err:
        print(f"err: {err}", file=sys.stderr)
    return None


def update_html(template_name, updates):
    if updates is not None:
        try:
            f = codecs.open(f"app/static/htmls/{template_name}", 'r')
            soup = bs4.BeautifulSoup(f.read(), features="html5lib")

            # soup = bs4.BeautifulSoup(f.read(), 'html.parser')
            for update in updates:
                print(update, file=sys.stderr)
                if update["type"] == "string":
                    soup.find(
                        "h1", {"id": update["id"]}).string = update["value"]
                elif update["type"] == "href":
                    soup.find("a", {"id": update["id"]})[
                        'href'] = update["value"]
                elif update["type"] == "textarea":
                    soup.find(
                        "textarea", {"id": update["id"]}).string = update["value"]
                elif update["type"] == "span":
                    soup.find(
                        "span", {"id": update["id"]}).string = update["value"]
                elif update["type"] == "img":
                    soup.find(
                        "img", {"id": update["id"]})['src'] = update["value"]

            updated_html = str(soup)
            return updated_html
        except Exception as err:
            print(f"err: {err}", file=sys.stderr)
    return None

#endregion helper functions


@api_blueprint.route('/sample_call', methods=['GET'])
def sample_page():

    ret = {"sample return": 10}
    return(jsonify(ret), 200)


@api_blueprint.route('/update_schedule/<s_id>', methods=['POST'])
def update_schedule(s_id):
    # return(jsonify({"Error":"err"}), 400) # show error test
    schedule = models.Schedule.query.get(s_id)
    if not schedule:
        return(jsonify({"result": "Error"}), 404)
    if schedule.calendarId != 1:
        return(jsonify({"result": "Invoice status is not In-Progress."}), 400)
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
        schedule.title = title
    if location is not None:
        schedule.location = location
    if dnotes is not None:
        schedule.dnotes = dnotes
    if start is not None:
        schedule.start = datetime.datetime.strptime(
            start['_date'], '%Y-%m-%dT%H:%M:%S.%f%z').astimezone(pytz.timezone('Asia/Karachi'))
    if end is not None:
        schedule.end = datetime.datetime.strptime(
            end['_date'], '%Y-%m-%dT%H:%M:%S.%f%z').astimezone(pytz.timezone('Asia/Karachi'))
    if isAllDay is not None:
        schedule.isAllDay = isAllDay
    if state is not None:
        schedule.state = state
    if isPrivate is not None:
        schedule.isPrivate = isPrivate

    db.session.commit()

    ret = {"sample return": 10}
    return(jsonify(ret), 200)


@api_blueprint.route('/complete_schedule/<s_id>', methods=['POST'])
def complete_schedule(s_id):
    # return(jsonify({"Error":"err"}), 400) # show error test
    schedule = models.Schedule.query.get(s_id)
    if not schedule:
        return(jsonify({"result": "Error"}), 404)
    if schedule.calendarId != 1:
        return(jsonify({"result": "Invoice status is not In-Progress."}), 400)

    post_data = json.loads(request.get_data())
    print("post_data")
    print(post_data)
    # {'title': 'First2', 'location': 'Summary2 is', 'dnotes': 'Needs surgeryss2', 'start': {'_date': '2022-07-20T07:00:00.000Z'}, 'end': {'_date': '2022-07-21T19:00:00.000Z'}, 'isAllDay': False, 'state': 'Free'}

    price = post_data.get("price", None)

    if not price:
        return(jsonify({"result": "Param missing"}), 404)

    schedule.price = price
    schedule.calendarId = 2

    db.session.commit()

    template_name = invoice_html
    updates = [
        {
            "id": "invoice",
            "type": "href",
            "value": "yoyo"
        }
    ]
    html = update_html(template_name=template_name, updates=updates)
    if html:
        pdf = generate_pdf_from_html(
            models.HtmlType.String.value, f"Invoice_{s_id}.html", html)
        if pdf:
            return send_file(pdf[4:], as_attachment=True), 200

    return jsonify({"status": "fail", "err": "Invoice could not be generated."}), 400


# @api_blueprint.route('/download_schedule/<s_id>', methods=['GET'])
# def download_schedule(s_id):
@api_blueprint.route('/download_schedule/<s_id>', methods=['GET'])
def download_schedule(s_id):
    # return(jsonify({"Error":"err"}), 400) # show error test
    schedule = models.Schedule.query.get(s_id)
    if not schedule:
        return(jsonify({"result": "Error"}), 404)
    if schedule.calendarId != 2:
        return(jsonify({"result": "Invoice status is not Completed."}), 400)

    filename = f"static/htmls/Invoice_{s_id}.pdf"
    from pathlib import Path
    if not Path('app/'+filename).exists():
        return(jsonify({"result": "File does not exist."}), 404)

    print(f"Downloading file: {filename}")
    return send_file(filename, as_attachment=True), 200


@api_blueprint.route('/cancel_schedule/<s_id>', methods=['POST'])
def cancel_schedule(s_id):
    # return(jsonify({"Error":"err"}), 400) # show error test
    schedule = models.Schedule.query.get(s_id)
    if not schedule:
        return(jsonify({"result": "Error"}), 404)
    if schedule.calendarId != 1:
        return(jsonify({"result": "Invoice status is not In-Progress."}), 400)

    schedule.calendarId = 3

    db.session.commit()

    ret = {"sample return": 10}
    return(jsonify(ret), 200)


@api_blueprint.route('/create_schedule', methods=['POST'])
def create_schedule():
    post_data = json.loads(request.get_data())
    print("post_data")
    print(post_data)

    title = post_data.get("title", None)
    calendarId = int(post_data.get("calendarId", None))
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


# @api_blueprint.route('/delete_schedule/<s_id>', methods=['POST'])
# def delete_schedule(s_id):
#     models.Schedule.query.filter_by(id=s_id).delete()
#     db.session.commit()
#     return(jsonify({"status": "success"}), 200)


@api_blueprint.route('/testfile', methods=["GET"])
def test_just_file_s():
    template_name = test
    updates = [
        {
            "id": "invoice",
            "type": "href",
            "value": "yoyo"
        }
    ]
    html = update_html(template_name=template_name, updates=updates)
    if html:
        filed = generate_pdf_from_html(
            models.HtmlType.String.value, "testfile.html", html)
        if filed:
            return send_file(filed[4:], as_attachment=True), 200

    return jsonify({"status": "fail", "err": "Invoice could not be generated."}), 400
