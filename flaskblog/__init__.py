from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt  # type: ignore
from flask_login import LoginManager  # type: ignore
from flask_mail import Mail
from flaskblog.config import Config
import humanize
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Add humanize filter
    @app.template_filter("humanize")
    def humanize_time(dt):
        if isinstance(dt, datetime):
            return humanize.naturaltime(datetime.now() - dt)
        return dt

    from flaskblog.users.routes import users  # noqa: E402
    from flaskblog.posts.routes import posts  # noqa: E402
    from flaskblog.main.routes import main  # noqa: E402
    from flaskblog.errors.handlers import errors  # noqa: E402

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
