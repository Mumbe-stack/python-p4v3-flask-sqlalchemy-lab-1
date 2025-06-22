from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app
from models import db

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Set up the Manager
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
