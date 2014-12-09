from settings_common import *

config.read('%s/settings/config/settings_dev.cfg' % BASE_DIR)

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': config.get('databases', 'engine'),
        'NAME': config.get('databases', 'name'),
        'USER': config.get('databases', 'user'),
        'PASSWORD': config.get('databases', 'password'),
        'HOST': config.get('databases', 'host'),
        'PORT': config.get('databases', 'port'),
    }
}
