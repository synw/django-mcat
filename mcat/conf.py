# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', User)

USE_PRICES = getattr(settings, 'MCAT_USE_PRICES', True)
CURRENCY = getattr(settings, 'MCAT_CURRENCY', '$')
PRICES_AS_INTEGER = getattr(settings, 'MCAT_PRICES_AS_INTEGER', False)

DISABLE_BREADCRUMBS = getattr(settings, 'MCAT_DISABLE_BREADCRUMBS', False)

CARACTERISTIC_TYPES = (
                        ('choices', _(u'Choices')),
                        ('boolean', _(u'Yes / No')),
                        ('int', _(u'Numeric')),
                       )

FILTERS_POSITION = getattr(settings, 'MCAT_FILTERS_POSITION', 'side')