import os
import dj_database_url

from .settings import *

SECRET_KEY = os.environ.get('SECRET_KEY')

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'))}

DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = [
    os.environ.get('ALLOWED_HOSTS'),
    'localhost',
    '127.0.0.1',
    'your-place.westus.cloudapp.azure.com']

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
