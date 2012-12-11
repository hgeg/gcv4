# Django settings for gma project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Ali Can Bulbul', 'alicanblbl@gmail.com'),
)

AUTH_PROFILE_MODULE = "gma.UserProfile"

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'gma_database_test'   # Or path to database file if using sqlite3.
DATABASE_USER = 'root'             # Not used with sqlite3.
DATABASE_PASSWORD = 'sokoban'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Istanbul'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True


# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = 'http://gcv4.s3.amazonaws.com/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://gcv4.s3.amazonaws.com/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '*=ku-2ei^%0nwj&0_y*qe^h227g(&iwtrm0o^&ot=t*x@k+f-@'


#E-mail settings
EMAIL_USE_TLS       = True
EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_HOST_USER     = 'alicanblbl@gmail.com'
EMAIL_HOST_PASSWORD = '******'
EMAIL_PORT          = 587

#Pusher app settings
APP_ID     = '20374'
APP_KEY    = '2db61f16f86947ae603e'
APP_SECRET = '491bf979f3b0da949aef'

#MongoDB settings
MONGODB_NAME = "gcv4_spell_db"
MONGODB_ADDRESS = "dbh45.mongolab.com:27457"
MONGODB_USER = "spells_user_readonly"
MONGODB_PASSWORD = "B3VdfZrwqd7gGmYkCMngjWw8"

#Amazon S3 settings
S3_PUBLIC_BUCKET = "http://gcv4.s3.amazonaws.com/files/"


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'gma.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #"/home/gma/www/gma/public/templates/"
    "./public/templates/"
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'gma.game'
)
