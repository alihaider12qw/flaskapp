from flask_migrate import MigrateCommand
from flask_script import Manager

from app import create_app
from app.commands import InitDbCommand

if __name__ == "__main__":
    manager = Manager(create_app)
    manager.add_command('db', MigrateCommand)
    manager.add_command('init_db', InitDbCommand)
    manager.run()
