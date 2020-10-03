from flask import Flask
from os import getenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    DB_URL = f"postgresql+psycopg2://{getenv('DB_USER')}:{getenv('DB_PASSWORD')}@{getenv('DB_URL')}/{getenv('DB_DATABASE')}"

    app.config["SECRET_KEY"] = getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # Models
        from .models.userModel import UsersModel

        # Import Blueprints
        from .controllers.controller_login import login_bp
        from .controllers.controller_user import user_bp

        # Register Blueprints to App
        app.register_blueprint(login_bp)
        app.register_blueprint(user_bp)

    return app
