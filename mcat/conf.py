# -*- coding: utf-8 -*-

from django.conf import settings


USE_PRICES = getattr(settings, 'MCAT_USE_PRICES', True)
CURRENCY = getattr(settings, 'MCAT_CURRENCY', '$')
PRICES_AS_INTEGER = getattr(settings, 'MCAT_PRICES_AS_INTEGER', False)

DISABLE_BREADCRUMBS = getattr(settings, 'MCAT_DISABLE_BREADCRUMBS', False)
