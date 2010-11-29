# Django settings for codedependant project.
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEVLOPMENT_MODE = True 
MAINTENANCE_MODE = False

if DEVLOPMENT_MODE:

    DEBUG = True
    TEMPLATE_DEBUG = True
    TEMPLATE_STRING_IF_INVALID = ''
#    CACHE_BACKEND = 'locmem:///'
    SESSION_EXPIRE_AT_BROWSER_CLOSE = False
    
else:
    DEBUG = False
    TEMPLATE_DEBUG = False
    TEMPLATE_STRING_IF_INVALID = ''
    CACHE_BACKEND= 'dummy:///' 
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS
APPEND_SLASH = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'codedependant',                      # Or path to database file if using sqlite3.
        'USER': 'postgres',                      # Not used with sqlite3.
        'PASSWORD': 'qxm8uavi',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
DJAPIAN_DATABASE_PATH = './djapian_spaces'
REDIS_HOST='localhost'
REDIS_DB = 0
REDIS_PORT = 6379
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'
DJAPIAN_DATABASE_PATH = './djapian_spaces'
# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = PROJECT_ROOT + '/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"

MEDIA_URL = 'http://127.0.0.1:8000/static_media/'
STATIC_DOC_ROOT = 'media/'
ADMIN_MEDIA_PREFIX = '/media/'
SESSION_ENGINE = 'sessions.backends.pyredis'
# Make this unique, and don't share it with anybody.
SECRET_KEY = '-2*z^98odz6vl%g2n_z)@9)9=1k&9b$wk-qnhuj2-o*%jlc5hu'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'maintenancemode.middleware.MaintenanceModeMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'codedependant.urls'
INTERNAL_IPS = ('127.0.0.1',)
TEMPLATE_DIRS = (
    PROJECT_ROOT +'/templates/'
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
#    'hitmen.context_processors.teammate',    
)
INSTALLED_APPS = (
#    'grappelli',
    'debug_toolbar',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.flatpages',    
    'django.contrib.sitemaps',  
    'django.contrib.comments',
    'codedependant.core',
    'codedependant.publisher',
    'django_extensions',
    'registration',
    'django_messages',
    'maintenancemode',
    'djapian',
    'pagination',
    'sorl.thumbnail',
    'photologue',
    'south',
    'queryset_transform',
    'hotsauce',
    
)
