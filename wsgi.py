# from manage import manager as app
 
# if __name__ == '__main__':
#    app.run()

# # # from app import app

# # from flask_migrate import MigrateCommand
# # from flask_script import Manager

from app import create_app, db
from flask.cli import FlaskGroup
import datetime
from app.models.user_models import *
# # from app.commands import InitDbCommand

# # # Setup Flask-Script with command line commands
# # app = Manager(create_app)
# # app.add_command('db', MigrateCommand)
# # app.add_command('init_db', InitDbCommand())

# app = create_app()
# cli = FlaskGroup(create_app=create_app)


# @cli.command()
# def recreate_db():
#     db.drop_all()
#     db.create_all()

#     db.session.commit()


# if __name__ == "__main__":
#     cli()
#     app.run(host='0.0.0.0', debug=True)
app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    doctor = Doctor(name="Dr. John Doe",
                    profession="Heart Surgeon",
                    profile_picture_url="doc5.jpeg",
                    qualification="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
                    charges=700)
    db.session.add(doctor)

    schedule = Schedule("1", "First", "Summary is", "Needs surgery", datetime.datetime.now(), datetime.datetime.now(), True, False, "Busy", 1)
    db.session.add(schedule)


    db.session.commit()


if __name__ == '__main__':
    cli()
    app.run(host='0.0.0.0', debug=True)
