# Django settings for UltraWeb project.
import os, sys

#-------------------------------------------------------------------------------
def rel(*x):
    """ A portable way to deal with production/development server runs """
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
#-------------------------------------------------------------------------------
def which_config(file, default="prod"):
    """ a helper function to peek @ settings_default and read in the user we want."""
    try:
        f = open(file)
        try:
            for line in f.readlines():
                tok=0
                tok = line.split("#")[0].strip()
                if (tok):
                    return tok
        finally:
            f.close()
    except IOError, msg:
        print >> sys.stderr, "settings.which_config: Can't read", file, ':', msg
        return(default)
    return default

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
config_name = which_config(ROOT_PATH + '/settings_default')

configs = {
    'jds'   : 'settings_jds',
    'bruhl' : 'settings_bruhl',
    'swhite': 'settings_swhite',
    'prod'  : 'settings_prod',
    'plain'  : 'settings_plain',
}

DJANGO_SETTINGS_MODULE = ROOT_PATH # this makes the imports work
BASE_DIR = ROOT_PATH # from project home settings.py
PROJECT_DIR = BASE_DIR
MEDIA_ROOT = rel('media')
STATIC_DOC_ROOT = MEDIA_ROOT

TEMPLATE_CONTEXT_PROCESSORS=(#"django.core.context_processors.auth",
                             "django.contrib.auth.context_processors.auth",
                             "django.core.context_processors.debug",
                             "django.core.context_processors.i18n",
                             "django.core.context_processors.media",
                             "django.contrib.messages.context_processors.messages",
                             "django.core.context_processors.request",)


ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'uh#xol!j99d402jid&bs_y%8ur8*=emk_hnw6f4cbvqn%*g4vq'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'weblogging.middleware.logging.WebLoggingMiddleware',
)

LOGGING_MIDDLEWARE_ENABLED=True

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    rel('templates'),
    rel('api/templates'),
    rel('weblogging/templates'),
    rel('realview/templates')
)
FIXTURE_DIRS = (
    # Note: platformIdentity/fixtures && core/fixtures && l16/nad/fixtures
    #       are automatically picked up by the system, we want to ensure that
    #       this dir gets picked up after the core/fixtures one.
    rel('fixtures'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'api',
    'weblogging',
    'realview',
    'config'
)

SERIALIZATION_MODULES = {
    'json': 'wadofstuff.django.serializers.json'
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

def needleInHayStack(haystack, needle):
    """
    Utility function to keep us from loading env variables if they are already set.
    haystack is a list and needle is a string
    """
    for itm in haystack:
        if itm.find(needle) == 0:
            return True
    return False

### ############################################################################
### Note: dynamic settings loading
###       Import the configuration settings file - REPLACE projectname with your project
###       this gives us a chance to append or step-on variables.
### ############################################################################
config_module = __import__('config.%s' % configs[config_name], globals(), locals(), 'UltraWeb')

# Load the config settings properties into the local scope.
for setting in dir(config_module):
    if setting == setting.upper():
        locals()[setting] = getattr(config_module, setting)

# Here we are going to log some stuff so we can examine the differences between runnint
# in devel mode vs WSGi mode.
# http://blog.dscpl.com.au/2010/03/improved-wsgi-script-for-use-with.html
try: 
    fh = open('/tmp/django_debug.txt', "a")
    from distutils.sysconfig import get_python_lib
    import datetime
    fh.write("------------------------ %s --------------------------------\n" % (datetime.datetime.now().isoformat(' ')))
    fh.write("\n")
    fh.write("__name__ = %s\n" % __name__)
    fh.write("__file__ = %s\n" % __file__)
    fh.write("os.getpid() = %s\n" % os.getpid())
    fh.write("os.getcwd() = %s\n" % os.getcwd())
    fh.write("os.curdir = %s\n" % os.curdir)
    fh.write("sys.path = %s\n\n" % repr(sys.path))
    fh.write("sys.modules.keys() = %s\n\n" % repr(sys.modules.keys()))
    fh.write("sys.modules.has_key('UltraWeb') = %s\n" % sys.modules.has_key('UltraWeb'))
    if sys.modules.has_key('UltraWeb'):
        fh.write("sys.modules['UltraWeb'].__name__ = %s\n" % sys.modules['UltraWeb'].__name__)
        fh.write("sys.modules['UltraWeb'].__file__ = %s\n" % sys.modules['UltraWeb'].__file__)
        fh.write("os.environ['DJANGO_SETTINGS_MODULE'] = %s\n" % os.environ.get('DJANGO_SETTINGS_MODULE', None))
    fh.write("python lib path: %s \n" % get_python_lib())
    fh.close()
except:
    pass

