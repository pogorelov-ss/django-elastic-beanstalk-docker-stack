import os
import sys

##################################################################
# Application configuration
##################################################################
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.dirname(BASE_DIR)
DATA_DIR = os.environ.get('INSTANCE_DATA_DIR', PROJECT_DIR)
print(BASE_DIR, PROJECT_DIR, DATA_DIR)
sys.path.append(os.path.join(PROJECT_DIR, 'libs'))
import secrets

SECRETS = secrets.getter(os.path.join(DATA_DIR, 'secrets.json'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRETS['secret_key']
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJ_DEBUG', False)

##################################################################
# ALLOWED_HOSTS Hack
##################################################################
ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOST'), 'www.{}'.format(os.environ.get('ALLOWED_HOST'))]
import requests

EC2_PRIVATE_IP = None
try:
    EC2_PRIVATE_IP = requests.get('http://169.254.169.254/latest/meta-data/local-ipv4', timeout=0.01).text
except requests.exceptions.RequestException:
    pass

if EC2_PRIVATE_IP:
    ALLOWED_HOSTS.append(EC2_PRIVATE_IP)
##################################################################

ROOT_URLCONF = 'dj_main.urls'

WSGI_APPLICATION = 'dj_main.wsgi.application'

##################################################################
# CACHE settings
##################################################################
CACHE_HOST = os.environ.get('CACHE_HOST', 'redis')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': '{}:6379'.format(CACHE_HOST),
    }
}
##################################################################
# Celery settings $ celery -A dj_main worker -l info
##################################################################
BROKER_URL= 'redis://{}:6379/2'.format(CACHE_HOST)
BROKER_TRANSPORT_OPTIONS = {
    'visibility_timeout': 3600,
    'fanout_prefix': True,
    'fanout_patterns': True
}
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
##################################################################
# DJANGO REST FRAMEWORK CONFIG
##################################################################
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning'
}
##################################################################
# Databases settings
##################################################################

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('RDS_DB_NAME'),
        'USER': os.environ.get('RDS_USERNAME'),
        'PASSWORD': os.environ.get('RDS_PASSWORD'),
        'HOST': os.environ.get('RDS_HOSTNAME'),
        'PORT': os.environ.get('RDS_PORT')
    }
}
##################################################################
# Language and timezone settings
##################################################################

# Specifies whether Django's translation system should be enabled.
USE_I18N = True

# Specifies if localized formatting of data will be enabled by
# default or not.
USE_L10N = True

# Specifies if datetimes will be timezone-aware by default or not.
USE_TZ = True

# A string representing the time zone for this installation.
TIME_ZONE = 'UTC'

# A string representing the language code for this installation.
LANGUAGE_CODE = 'en-us'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

##################################################################
# Installed apps
##################################################################

EXTERNAL_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Other external apps
    'raven.contrib.django.raven_compat',
    'celery',
    'rest_framework',
]


INTERNAL_APPS = [

]

INSTALLED_APPS = EXTERNAL_APPS + INTERNAL_APPS

##################################################################
# Middleware settings
##################################################################

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


##################################################################
# Templates settings
##################################################################

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

##################################################################
# Static settings
##################################################################

STATIC_ROOT = os.path.join(PROJECT_DIR, 'collect/static/')
# MEDIA_ROOT = PROJECT_DIR.child("media")

# URL to use when referring to static files located in STATIC_ROOT.
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
##################################################################
# DEBUG settings
##################################################################
if DEBUG:
    ALLOWED_HOSTS = ['*']
    ##################################################################
    # uwsgi autoreload
    ##################################################################
    try:
        import uwsgi
        from uwsgidecorators import timer
        from django.utils import autoreload


        @timer(3)
        def change_code_gracefull_reload(sig):
            if autoreload.code_changed():
                uwsgi.reload()
    except Exception as error:
        print('we are on localhost ', error)

    ##################################################################
    # apps
    ##################################################################
    INSTALLED_APPS += (
        # 'debug_toolbar',
        'django_extensions',
    )