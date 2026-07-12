from flask import Flask

from config import Config
from ext import db, migrate, cors


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    from routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app
