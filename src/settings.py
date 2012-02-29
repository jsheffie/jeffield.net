# Django settings for jeffield project.
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
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
MEDIA_URL = '/media/'
STATIC_ROOT = ''
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = 'uh#xol!j99d402jid&bs_y%8ur8*=emk_hnw6f4cbvqn%*g4vq'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

LOGGING_MIDDLEWARE_ENABLED=True

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    rel('templates'),
)
FIXTURE_DIRS = (
    rel('fixtures'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
)

SERIALIZATION_MODULES = {
    'json': 'wadofstuff.django.serializers.json'
}

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
config_module = __import__('config.%s' % configs[config_name], globals(), locals(), 'jeffield')

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
    fh.write("sys.modules.has_key('jeffield') = %s\n" % sys.modules.has_key('jeffield'))
    if sys.modules.has_key('jeffield'):
        fh.write("sys.modules['jeffield'].__name__ = %s\n" % sys.modules['jeffield'].__name__)
        fh.write("sys.modules['jeffield'].__file__ = %s\n" % sys.modules['jeffield'].__file__)
        fh.write("os.environ['DJANGO_SETTINGS_MODULE'] = %s\n" % os.environ.get('DJANGO_SETTINGS_MODULE', None))
    fh.write("python lib path: %s \n" % get_python_lib())
    fh.close()
except:
    pass

