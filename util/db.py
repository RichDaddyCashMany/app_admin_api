from flask_sqlalchemy import SQLAlchemy


class DB:
    session = None

    @classmethod
    def init(cls, app):
        db = SQLAlchemy()
        db.init_app(app)
        cls.session = db.session
