import os
import dj_database_url
from .common import *

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = ['housify-prod.herokuapp.com']

DATABASES = {
    'default': dj_database_url.config()
}
