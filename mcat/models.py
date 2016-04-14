# -*- coding: utf-8 -*-

from collections import OrderedDict
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from mptt.models import TreeForeignKey, MPTTModel
import django_filters
from mbase.models import default_statuses, OrderedModel, MetaBaseModel, MetaBaseUniqueSlugModel, MetaBaseNameModel, MetaBaseStatusModel
from mqueue.models import MonitoredModel
from mcat.forms import FilterForm
from mcat.conf import USE_PRICES, PRICES_AS_INTEGER, CARACTERISTIC_TYPES


STATUSES = getattr(settings, 'STATUSES', default_statuses)
    

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
    carac1 = models.CharField(max_length=255, verbose_name=_(u'Caracteristic 1'))
    carac2 = models.CharField(max_length=255, verbose_name=_(u'Caracteristic 2'))
    carac3 = models.CharField(max_length=255, verbose_name=_(u'Caracteristic 3'))
    carac4 = models.CharField(max_length=255, verbose_name=_(u'Caracteristic 4'))
    carac5 = models.CharField(max_length=255, verbose_name=_(u'Caracteristic 5'))
    carac6 = models.CharField(max_length=255, verbose_name=_(u'Caracteristic 6'))
    carac7 = models.CharField(max_length=255, verbose_name=_(u'Caracteristic 7'))
    carac8 = models.CharField(max_length=255, verbose_name=_(u'Caracteristic 8'))
    
    class Meta:
        verbose_name=_(u'Product')
        verbose_name_plural =_( u'Products')
        ordering = ('name','created')

    def __unicode__(self):
        return unicode(self.name)
    
    def save(self, *args, **kwargs):
        i = 1
        for carac in self.caracteristics.all():
            if i == 1:
                self.carac1 = carac.name+':'+unicode.strip(carac.value)
            if i == 2:
                self.carac2 = carac.name+':'+unicode.strip(carac.value)
            if i == 3:
                self.carac3 = carac.name+':'+unicode.strip(carac.value)
            if i == 4:
                self.carac4 = carac.name+':'+unicode.strip(carac.value)
            if i == 5:
                self.carac5 = carac.name+':'+unicode.strip(carac.value)
            if i == 6:
                self.carac6 = carac.name+':'+unicode.strip(carac.value)
            if i == 7:
                self.carac7 = carac.name+':'+unicode.strip(carac.value)
            if i == 8:
                self.carac8 = carac.name+':'+unicode.strip(carac.value)
            i += 1
        super(Product, self).save()
    
    def get_price(self):
        price = None
        if USE_PRICES:
            price = self.price
            if PRICES_AS_INTEGER:
                price = int(round(price))
        return price
    
    
class ProductImage(MetaBaseModel, MetaBaseStatusModel, OrderedModel):
    image = models.ImageField(upload_to='products', verbose_name=_(u'Image'))
    #~ external key
    product = models.ForeignKey(Product, related_name="images", verbose_name=_(u'Product'))
    
    class Meta:
        verbose_name=_(u'Product image')
        verbose_name_plural = _(u'Product images')

    def __unicode__(self):
        return unicode(self.image.url)


class ProductCaracteristic(MetaBaseModel, MetaBaseNameModel):
    product = models.ForeignKey(Product, related_name="caracteristics", verbose_name=_(u'Product'))
    value = models.CharField(max_length=255, verbose_name=_(u'Value'))

    class Meta:
        verbose_name=_(u'Product caracteristic')
        verbose_name_plural =_( u'Product caracteristics')
        ordering = ('name', 'created')

    def __unicode__(self):
        return unicode(self.name)
    
    
class CategoryCaracteristic(MetaBaseModel, MetaBaseNameModel, MetaBaseUniqueSlugModel, OrderedModel):
    category = models.ForeignKey(Category, related_name="generic_caracteristics", verbose_name=_(u'Category'))
    type = models.CharField(max_length=255, choices=CARACTERISTIC_TYPES, default=CARACTERISTIC_TYPES[0][0])
    choices = models.TextField(blank=True, verbose_name=_(u'Choices'))
    
    class Meta:
        verbose_name=_(u'Caracteristic for category')
        verbose_name_plural =_( u'Caracteristics for category')

    def __unicode__(self):
        return unicode(self.name)

    def get_choices(self):
        choices = OrderedDict()
        for choice in self.choices.split('\n'):
            splited = choice.split('>')
            val = unicode.strip(splited[0])
            slug = unicode.strip(splited[1])
            choices[slug] = val
        return choices
    

            
        
        


