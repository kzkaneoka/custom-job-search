import os

from flask import Flask
from flask_admin import Admin
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


admin = Admin(template_mode="bootstrap3")
bcrypt = Bcrypt()
cors = CORS()
db = SQLAlchemy()


def create_app(script_info=None):

    app = Flask(__name__)

    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    bcrypt.init_app(app)
    cors.init_app(app)
    db.init_app(app)
    if os.getenv("FLASK_ENV") == "development":
        admin.init_app(app)

    from project.api.auth import auth_blueprint
    from project.api.ping import ping_blueprint
    from project.api.users.views import users_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(ping_blueprint)
    app.register_blueprint(users_blueprint)

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
