from .settings import *

ALLOWED_HOSTS = ['.saeedrila.dev', 'saeedrila.dev', 'www.saeedrila.dev']
CSRF_TRUSTED_ORIGINS = ['https://saeedrila.dev', 'https://www.saeedrila.dev']

SESSION_COOKIE_SECURE = True

LOGIN_REDIRECT_URL = 'home'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/myapp.log',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}