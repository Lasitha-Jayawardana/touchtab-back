import os
from pydantic import BaseSettings

from utilities.logger import logger


class Credentials(BaseSettings):
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_CHARSET: str

    TWILIO_ACCOUNT_SID: str = None
    TWILIO_AUTH_TOKEN: str = None
    TWILIO_NUMBER: str = None

    # EMAIL_SMTP_SERVER: str
    # EMAIL_PORT: int
    # EMAIL_SENDER_EMAIL: str
    # EMAIL_PASSWORD: str
    #
    AUTHENTICATION_SECRET: str
    AUTHENTICATION_MECHANISM: str
    REFRESH_TOKEN_EXPIRY: int  # Days
    ACCESS_TOKEN_EXPIRY: int  # Minutes
    RESET_TOKEN_EXPIRY: int

    class Config:
        if os.getenv('MODE') == 'prod':
            env_file = 'credentials/Prod.env'
            logger.debug("Production environment activated!")
        else:
            env_file = 'credentials/Dev.env'
            logger.debug("Development environment activated!")
        env_file_encoding = 'utf-8'


# Sets the environment Credentials from the variables.
CREDENTIALS = Credentials()

if __name__ == "__main__":
    logger.debug(CREDENTIALS.dict())
