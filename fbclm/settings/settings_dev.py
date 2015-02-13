"""
Copyright 2015 Smart Studio.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from fbclm.settings.settings_common import *

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
