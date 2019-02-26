from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.app import get_app
from app.models.__init__ import db


app = get_app()
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
