# -*- coding: utf-8 -*-

from collections import OrderedDict
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from mptt.models import TreeForeignKey, MPTTModel
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
    

def is_val_in_field(val, field_val):
    val = val.split(':')[0]
    name = field_val.split(':')[0]
    if val == name:
        return True
    return False


class ProductCaracteristic(MetaBaseModel, MetaBaseNameModel):
    product = models.ForeignKey(Product, related_name="caracteristics", verbose_name=_(u'Product'))
    value = models.CharField(max_length=255, verbose_name=_(u'Value'))

    class Meta:
        verbose_name=_(u'Product caracteristic')
        verbose_name_plural =_( u'Product caracteristics')
        ordering = ('name', 'created')

    def __unicode__(self):
        return unicode(self.name)
    
    def save(self, *args, **kwargs):
        product = self.product
        val = self.name+':'+unicode.strip(self.value)
        field = False
        if product.carac1 == '' or is_val_in_field(val, product.carac1):
            product.carac1 = val
            field = True
            print 'Field 1'
        if not field and product.carac2 == '' or is_val_in_field(val, product.carac2):
            product.carac2 = val
            field = True
        if not field and product.carac3 == '' or is_val_in_field(val, product.carac3):
            product.carac3 = val
            field = True
        if not field and product.carac4 == '' or is_val_in_field(val, product.carac4):
            product.carac4 = val
            field = True
        if not field and product.carac5 == '' or is_val_in_field(val, product.carac5):
            product.carac5 = val
            field = True
        if not field and product.carac6 == '' or is_val_in_field(val, product.carac6):
            product.carac6 = val
            field = True
        if not field and product.carac7 == '' or is_val_in_field(val, product.carac7):
            product.carac7 = val
            field = True
        if not field and product.carac8 == '' or is_val_in_field(val, product.carac8):
            product.carac8 = val
        product.save()
        super(ProductCaracteristic, self).save()
    
    
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
    

            
        
        


