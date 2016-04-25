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

TEMPLATE_NAMES = (
                    ('default',_(u'Filters on side')),
                    ('filters_on_top',_(u'Filters on top')),
                    ('fullwidht_filters_on_top',_(u'Fullwidth filters on top')),
                    )

USE_FILTERS = getattr(settings, 'MCAT_USE_FILTERS', True)

USE_PRICE_FILTER = getattr(settings, 'MCAT_USE_PRICE_FILTER', True)

CODE_MODE = getattr(settings, 'MCAT_CODE_MODE', False)

USE_ADMIN_BOOTSTRAPED = getattr(settings, 'MCAT_USE_ADMIN_BOOTSTRAPED', False)

USE_ORDER = 'mcat_order' in settings.INSTALLED_APPS

USE_BRAND = getattr(settings, 'MCAT_USE_BRAND', False)

PAGINATE_BY = getattr(settings, 'MCAT_PAGINATE_BY', 10)

