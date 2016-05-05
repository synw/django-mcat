# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig
from watson import search as watson

class McatConfig(AppConfig):
    name = "mcat"
    verbose_name = _(u"Catalog")
    
    def ready(self):
        from mcat import signals
        product = self.get_model("Product")
        watson.register(product)

