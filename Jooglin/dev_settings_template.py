from Jooglin.settings import *

DEBUG = True

INSTALLED_APPS += ('debug_toolbar', 'debug_panel')
MIDDLEWARE_CLASSES += ('debug_panel.middleware.DebugPanelMiddleware',)