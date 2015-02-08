from fbclm.settings.settings_common import *

DEBUG = False
TEMPLATE_DEBUG = False

config.read('%s/settings/config/settings_prod.cfg' % BASE_DIR)

SECRET_KEY = config.get('security', 'secret_key')

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
