from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig

class McatConfig(AppConfig):
    name = "mcat"
    verbose_name = _(u"Catalog")
    
    def ready(self):
        from mcat import signals

    
