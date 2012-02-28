import sys, os
from settings import *
###############################################################################
# This should be the only variable you need to edit, to set up a dev env      #
# pointing to remote mysql [dbms], and ejabberd [xmpp] servers.               #                            
###############################################################################
LAB_HOST='localhost' 
DEBUG = True

TIME_ZONE = 'GMT'
TEMPLATE_DEBUG = DEBUG

###############################################################################
# Setting up dbms                                                             #
###############################################################################
DATABASES = {
#    'csoa': {
#        'NAME': 'CSOACFG',
#        'ENGINE': 'django.db.backends.mysql',
#        'USER': 'csoa',
#        'PASSWORD': 'csoa',
#        'HOST':LAB_HOST,  
#        'PORT':'3306'  
#    },
    'default': {
        'NAME': 'TRACKSTORE',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'ultraweb',
        'PASSWORD': 'ultraweb',
        'HOST':LAB_HOST,  
        'PORT':'3306'  
    }
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#        'NAME': '/home/jds/workspace/UltraWeb/src/sqlite.db', # Or path to database file if using sqlite3.
#        'USER': '',                      # Not used with sqlite3.
#        'PASSWORD': '',                  # Not used with sqlite3.
#        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#    }
}

###############################################################################
# Setting up additional INSTALLED_APPS                                        #
###############################################################################
# here is a somewhat complicated way to 'safely' add python modules items if 
# they exists on the system (remember: tuple's are immutable)
inst_apps = list(INSTALLED_APPS)
try: 
    import django_extensions
    if not needleInHayStack(inst_apps, "django_extensions"):
        inst_apps.append('django_extensions')
except ImportError:
    pass
try:
    import debug_toolbar
    if not needleInHayStack(inst_apps, "debug_toolbar"):
        inst_apps.append('debug_toolbar')
except ImportError:
    pass
INSTALLED_APPS=tuple(inst_apps)

###############################################################################
# Configuring debug_toolbar if its available                                  #
###############################################################################
try: 
    debug_toolbar
    from socket import gethostname, gethostbyname
    INTERNAL_IPS = ( '127.0.0.1', 
                     '172.16.98.145', 
                     '172.16.176.124', 
                     gethostbyname(gethostname())+":8000/",) # debug_toolbar
# Note: debug toolbar breaks the streaming middleware.
    midd_class = list(MIDDLEWARE_CLASSES)
    if not needleInHayStack(midd_class, "debug_toolbar.middleware.DebugToolbarMiddleware"):
        midd_class.append('debug_toolbar.middleware.DebugToolbarMiddleware') 
    # Remember: order of middleware is important, ( down-n-up, union)
    MIDDLEWARE_CLASSES=tuple(midd_class)

    DEBUG_TOOLBAR_CONFIG = {
                            'INTERCEPT_REDIRECTS': False,
                            #    'SHOW_TOOLBAR_CALLBACK': show_dbtoolbar,
                            }
except NameError:
    pass
    #print "Not Setting up debug_toolbar" # this print will go to the server error log in production


