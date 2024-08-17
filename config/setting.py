import os
from config.connect import dbuser, dbpass, dbhost, dbport, dbname

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'mysql+mysqlconnector://{dbuser}:{dbpass}@{dbhost}:{dbport}/{dbname}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False





