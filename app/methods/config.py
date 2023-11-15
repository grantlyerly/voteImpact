import os
from dotenv import load_dotenv

load_dotenv('.flaskenv')

API_KEY = os.environ.get('API_KEY')

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False