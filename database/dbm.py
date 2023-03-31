from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from database import Base
from utilities.logger import logger, extra
from env import CREDENTIALS


class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)

            cls._instance.db_user = CREDENTIALS.MYSQL_USER
            cls._instance.db_pass = CREDENTIALS.MYSQL_PASSWORD
            cls._instance.db_host = CREDENTIALS.MYSQL_HOST
            cls._instance.db_port = CREDENTIALS.MYSQL_PORT
            cls._instance.database = CREDENTIALS.MYSQL_DATABASE
            cls._instance.charset = CREDENTIALS.MYSQL_CHARSET

            cls._instance.engine = cls._instance._get_engine()

            cls._instance._import_entities()
            Base.metadata.create_all(cls._instance.engine)
            logger.debug("Meta created", extra=extra)

            cls._instance.SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=cls._instance.engine)
            logger.debug("Session factory created", extra=extra)

        return cls._instance

    def _get_db_string(self):
        db_string = 'mysql+pymysql://{}:{}@{}:{}/{}?charset={}' \
            .format(self.db_user, self.db_pass, self.db_host, self.db_port, self.database, self.charset)
        return db_string

    def _get_engine(self):
        connect_string = self._get_db_string()
        engine = create_engine(connect_string, echo=False, isolation_level='SERIALIZABLE', pool_recycle=3600,
                               future=True)
        logger.debug("Engine created", extra=extra)
        return engine

    @staticmethod
    def _import_entities():
        from models.user import User

    def get_test_session(self):
        """Use only for (unit) tests"""
        Session = scoped_session(self.SessionFactory)
        current_session = Session()
        return current_session

    @staticmethod
    def safe_commit(session):
        try:
            session.commit()
        except Exception as e:
            logger.exception("Commit failed:", extra=extra)
            session.rollback()
            session.flush()
