# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from mptt.models import TreeForeignKey, MPTTModel
from mbase.models import default_statuses, MetaBaseModel, MetaBaseUniqueSlugModel, MetaBaseNameModel, MetaBaseTitleModel, MetaBaseStatusModel
from mqueue.models import MonitoredModel
from mcat.conf import USE_PRICES, PRICES_AS_INTEGER


STATUSES = getattr(settings, 'STATUSES', default_statuses)
from django.contrib.auth.models import User
USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', User)
    

class Brand(MetaBaseModel, MetaBaseNameModel, MetaBaseStatusModel, MetaBaseUniqueSlugModel, MonitoredModel):
    image = models.ImageField(blank=True, upload_to='brands', verbose_name=_(u'Image'))
    
    class Meta:
        verbose_name=_(u'Brand')
        verbose_name_plural = _(u'Brands')

    def __unicode__(self):
        return unicode(self.name)
    

class Category(MPTTModel, MetaBaseModel, MetaBaseNameModel, MetaBaseStatusModel, MetaBaseUniqueSlugModel, MonitoredModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name=u'children', verbose_name=_(u'Parent category'))
    image = models.ImageField(null=True, upload_to='categories', verbose_name=_(u"Navigation image"))
    
    class Meta:
        verbose_name=_(u'Category')
        verbose_name_plural = _(u'Categories')

    def __unicode__(self):
        return unicode(self.name)


class Product(MetaBaseModel, MetaBaseNameModel, MetaBaseStatusModel, MetaBaseUniqueSlugModel, MonitoredModel):
    #~ base content
    short_description = models.CharField(blank=True, max_length=250, verbose_name=_(u'Short description'))
    description = RichTextField(blank=True, verbose_name=_(u'Description'))
    upc = models.CharField(blank=True, max_length=30, verbose_name=_(u'Universal Product Code'))
    navimage = models.ImageField(null=True, upload_to='products/nav/', verbose_name=_(u'Navigation image'))
    #~ external keys
    brand = models.ForeignKey(Brand, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_(u'Brand'))
    category = TreeForeignKey(Category, verbose_name=_(u'Category'))
    #~ prices
    price = models.FloatField(null=True, blank=True, verbose_name=_(u'Price'))
    discounted_price = models.FloatField(null=True, blank=True, verbose_name=_(u'Discounted price'))
    discounted_percentage = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_(u'Discount percentage'))
    
    class Meta:
        verbose_name=_(u'Product')
        verbose_name_plural =_( u'Products')
        ordering = ('name','created')

    def __unicode__(self):
        return unicode(self.name)
    
    def get_price(self):
        price = None
        if USE_PRICES:
            price = self.price
            if PRICES_AS_INTEGER:
                price = int(round(price))
        return price
    
    
class ProductImage(MetaBaseModel, MetaBaseStatusModel):
    image = models.ImageField(upload_to='products', verbose_name=_(u'Image'))
    order = models.PositiveSmallIntegerField(null=True, verbose_name=_(u'Order'))
    #~ external key
    product = models.ForeignKey(Product, related_name="images", verbose_name=_(u'Product'))
    
    class Meta:
        ordering = ('order', 'created')
        verbose_name=_(u'Product image')
        verbose_name_plural = _(u'Product images')

    def __unicode__(self):
        return unicode(self.image.url)







