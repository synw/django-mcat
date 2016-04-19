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
from mcat.conf import USE_PRICES, PRICES_AS_INTEGER, CARACTERISTIC_TYPES, FILTERS_POSITION
from mcat.utils import is_val_in_field, encode_ftype


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
    filters_position = models.CharField(max_length=60, choices=FILTERS_POSITION, default=FILTERS_POSITION[0][0])
    description = RichTextField(blank=True, verbose_name=_(u'Description'))
    
    class Meta:
        verbose_name=_(u'Category')
        verbose_name_plural = _(u'Categories')

    def __unicode__(self):
        return unicode(self.name)


class Product(MetaBaseModel, MetaBaseNameModel, MetaBaseStatusModel, MetaBaseUniqueSlugModel, MonitoredModel):
    #~ base content
    short_description = RichTextField(blank=True, verbose_name=_(u'Short description'))
    description = RichTextField(blank=True, verbose_name=_(u'Long description'))
    upc = models.CharField(blank=True, unique=True, max_length=30, verbose_name=_(u'Universal Product Code'))
    navimage = models.ImageField(null=True, upload_to='products/nav/', verbose_name=_(u'Navigation image'))
    #~ external keys
    brand = models.ForeignKey(Brand, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_(u'Brand'))
    category = TreeForeignKey(Category, verbose_name=_(u'Category'))
    #~ prices
    price = models.FloatField(null=True, blank=True, verbose_name=_(u'Price'))
    discounted_price = models.FloatField(null=True, blank=True, verbose_name=_(u'Discounted price'))
    discounted_percentage = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_(u'Discount percentage'))
    available = models.BooleanField(default=True, verbose_name=_(u'Available'))
    carac1 = models.CharField(max_length=255, blank=True, verbose_name=_(u'Caracteristic 1'))
    carac2 = models.CharField(max_length=255, blank=True, verbose_name=_(u'Caracteristic 2'))
    carac3 = models.CharField(max_length=255, blank=True, verbose_name=_(u'Caracteristic 3'))
    carac4 = models.CharField(max_length=255, blank=True, verbose_name=_(u'Caracteristic 4'))
    carac5 = models.CharField(max_length=255, blank=True, verbose_name=_(u'Caracteristic 5'))
    int_carac1 = models.IntegerField(null=True, blank=True, verbose_name=_(u'Integer caracteristic 1'))
    int_carac2 = models.IntegerField(null=True, blank=True, verbose_name=_(u'Integer caracteristic 2'))
    int_carac3 = models.IntegerField(null=True, blank=True, verbose_name=_(u'Integer caracteristic 3'))
    int_carac1_name = models.CharField(max_length=255, blank=True, verbose_name=_(u'Integer caracteristic 1 name'))
    int_carac2_name = models.CharField(max_length=255, blank=True, verbose_name=_(u'Integer caracteristic 2 name'))
    int_carac3_name = models.CharField(max_length=255, blank=True, verbose_name=_(u'Integer caracteristic 3 name'))
    
    
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


class ProductCaracteristic(MetaBaseModel, MetaBaseNameModel):
    product = models.ForeignKey(Product, related_name="caracteristics", verbose_name=_(u'Product'))
    type = models.CharField(max_length=255, verbose_name=_(u'Type'))
    type_name = models.CharField(max_length=255, verbose_name=_(u'Type name'))
    value = models.CharField(max_length=255, verbose_name=_(u'Value'))
    value_name = models.CharField(max_length=255, verbose_name=_(u'Value name'))

    class Meta:
        verbose_name=_(u'Product caracteristic')
        verbose_name_plural =_( u'Product caracteristics')
        ordering = ('name', 'created')

    def __unicode__(self):
        return unicode(self.name)
    
    def format_value(self, ftype):
        return self.name+':'+unicode.strip(self.value)+';'+ftype
    
    def save(self, *args, **kwargs):
        if self.pk:
            product = self.product
            carac_type = CategoryCaracteristic.objects.filter(slug=self.name)[0]
            ftype = carac_type.type
            self.value_name =  carac_type.get_value_name(self.value, ftype)
            #val = self.name+':'+unicode.strip(self.value)
            val = self.format_value(ftype)
            field = False
            if ftype in ['choices', 'boolean']:
                if product.carac1 == '' or is_val_in_field(val, product.carac1):
                    product.carac1 = val
                    field = True
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
            field = False
            if ftype == 'int':
                if not product.int_carac1 or product.int_carac1_name == self.name:
                    product.int_carac1 = int(self.value)
                    product.int_carac1_name = self.name
                    field = True
                if not field and not product.int_carac2 or product.int_carac2_name == self.name:
                    product.int_carac2 = int(self.value)
                    product.int_carac2_name = self.name
                    field = True
                if not field and not product.int_carac3 or product.int_carac3_name == self.name:
                    product.int_carac3 = int(self.value)
                    product.int_carac3_name = self.name
            product.save()
        super(ProductCaracteristic, self).save()
    
    
class CategoryCaracteristic(MetaBaseModel, MetaBaseNameModel, MetaBaseUniqueSlugModel, OrderedModel):
    category = models.ForeignKey(Category, related_name="generic_caracteristics", verbose_name=_(u'Category'))
    type = models.CharField(max_length=255, choices=CARACTERISTIC_TYPES, default=CARACTERISTIC_TYPES[0][0])
    choices = models.TextField(blank=True, verbose_name=_(u'Choices'))
    unit = models.CharField(max_length=255, blank=True)
    
    class Meta:
        verbose_name=_(u'Caracteristic for category')
        verbose_name_plural =_( u'Caracteristics for category')
        ordering = ['order']

    def __unicode__(self):
        return unicode(self.name)

    def get_choices(self):
        choices = OrderedDict()
        ftype = encode_ftype(self.type)
        for choice in self.choices.split('\n'):
            splited = choice.split('>')
            val = unicode.strip(splited[0])
            slug = unicode.strip(splited[1])
            choices[slug] = val+';'+ftype
        return choices
    
    def get_value_name(self, value, ftype):
        if ftype == 'choices':
            for choice in self.choices.split('\n'):
                splited = choice.split('>')
                slug = unicode.strip(splited[0])
                val = unicode.strip(splited[1])
                #print slug+' / '+str(value)+' > '+str(val)
                if slug == unicode.strip(value):
                    return val
        if ftype == 'boolean':
            return str(value)
        if ftype == 'int':
            if self.unit:
                return value+'&nbsp;'+self.unit
            else:
                return value
        return ''

            
        
        


