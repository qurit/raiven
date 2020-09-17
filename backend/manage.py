import flask_migrate as fm
from flask_script import Manager as ScriptManager

from api import app, db, config


migrate = fm.Migrate(app, db, directory=config.MIGRATION_DIR)
manager = ScriptManager(app)

manager.add_command(fm.MigrateCommand)

if __name__ == "__main__":
    manager.run()
