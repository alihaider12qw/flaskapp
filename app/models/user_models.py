# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>, Matt Hogan <matt@twintechlabs.io>

# from flask_user import UserMixin
# from flask_user.forms import RegisterForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from app import db
from sqlalchemy.sql import func
from enum import Enum


class Doctor(db.Model):
    __tablename__ = "doctor"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(256), nullable=False)
    profession = db.Column(db.String(128), nullable=False)
    profile_picture_url = db.Column(db.Text, nullable=True)
    qualification = db.Column(db.Text, nullable=True)
    charges = db.Column(db.Float, nullable=False)

    time_created = db.Column(db.DateTime(timezone=True),
                             server_default=func.now(), nullable=False)
    time_updated = db.Column(db.DateTime(
        timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __init__(self, name, profession, profile_picture_url, qualification, charges):
        self.name = name
        self.profession = profession
        self.profile_picture_url = profile_picture_url
        self.qualification = qualification
        self.charges = charges

    def to_json(self):
        json_obj = {
            'id': self.id,
            'name': self.name,
            'profession': self.profession,
            'profile_picture_url': self.profile_picture_url,
            'qualification': self.qualification,
            'charges': round(self.charges, 2),
        }
        return json_obj


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    fullname = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(128), unique=True,  nullable=False)
    password = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(128), nullable=False)
    date_of_birth = db.Column(db.String(128), nullable=False)
    speciality = db.Column(db.String(128), nullable=True)

    time_created = db.Column(db.DateTime(timezone=True),
                             server_default=func.now(), nullable=False)
    time_updated = db.Column(db.DateTime(
        timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __init__(self, fullname, email, password, phone, date_of_birth, speciality):
        self.fullname = fullname
        self.email = email
        self.password = password
        self.phone = phone
        self.date_of_birth = date_of_birth
        self.speciality = speciality

    def to_json(self):
        json_obj = {
            'id': self.id,
            'fullname': self.fullname,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'profile_picture_url': self.profile_picture_url,
            'sign_in_id': self.sign_in_id,
        }
        return json_obj


class Schedule(db.Model):
    __tablename__ = "schedules"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    calendarId = db.Column(db.Integer, server_default="1", nullable=True)
    title = db.Column(db.String(256), nullable=True)
    location = db.Column(db.String(256), nullable=True)
    dnotes = db.Column(db.String(256), nullable=True)
    end = db.Column(db.DateTime(timezone=True), nullable=True)
    start = db.Column(db.DateTime(timezone=True), nullable=True)
    isAllDay = db.Column(db.Boolean(), nullable=True)
    isPrivate = db.Column(db.Boolean(), nullable=True)
    state = db.Column(db.String(256), nullable=True)

    # calendarId: "1"
    # title: "name"
    # dnotes: "dnotes"
    # isAllDay: false
    # isPrivate: false
    # location: "summ"
    # state: "Busy"

    time_created = db.Column(db.DateTime(timezone=True),
                             server_default=func.now(), nullable=False)
    time_updated = db.Column(db.DateTime(
        timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    fk_user = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User, backref='user_messages',
                           lazy=True, foreign_keys=[fk_user])

    def __init__(self, calendarId, title, location, dnotes, end, start, isAllDay, isPrivate, state, fk_user):
        self.calendarId = calendarId
        self.title = title
        self.location = location
        self.dnotes = dnotes
        self.end = end
        self.start = start
        self.isAllDay = isAllDay
        self.isPrivate = isPrivate
        self.state = state
        self.fk_user = fk_user

    def to_json(self):
        json_obj = {
            'id': self.id,
            'calendarId': self.calendarId,
            'title': self.title,
            'location': self.location,
            'dnotes': self.dnotes,
            'end': self.end,
            'start': self.start,
            'isAllDay': self.isAllDay,
            'isPrivate': self.isPrivate,
            'state': self.state,
            'fk_user': self.fk_user,
            'user': self.user.to_json()
        }
        return json_obj


#enums

class HtmlType(Enum):
    File = 1
    String = 2

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
