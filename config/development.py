# coding: utf-8
from .default import Config


class DevelopmentConfig(Config):
    # App config
    DEBUG = True

    # SQLAlchemy config
    # SQLALCHEMY_DATABASE_URI = "postgresql://root:@localhost/planner-backend"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{Config.PROJECT_PATH}'/db/dev.db"
