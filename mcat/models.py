# -*- coding: utf-8 -*-

from collections import OrderedDict
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import TreeForeignKey, MPTTModel
from jsonfield import JSONField
from mbase.models import STATUSES, MetaBaseOrderedModel, MetaBaseModel, MetaBaseUniqueSlugModel, MetaBaseNameModel, MetaBaseStatusModel
from jssor.conf import SLIDESHOW_TYPES
from mcat.conf import USE_PRICES, PRICES_AS_INTEGER, CARACTERISTIC_TYPES, CATEGORY_TEMPLATE_NAMES, PRODUCT_TEMPLATE_NAMES
from mcat.utils import is_name_in_field, encode_ftype
from mcat.conf import DEAL_TYPES


class Deal(models.Model):
    # type
    deal_type = models.CharField(max_length=120, verbose_name=_(u"Deal type"), choices=DEAL_TYPES, default=DEAL_TYPES[0][0])
    # offer
    discounted_price = models.FloatField(blank=True, null=True, verbose_name=_(u'Discounted price'))
    discounted_percentage = models.FloatField(blank=True, null=True, verbose_name=_(u'Discounted percentage'))
    deal_description = models.TextField(blank=True, verbose_name=_(u'Description'))
    # limitations
    deal_start_date = models.DateTimeField(blank=True, null=True, verbose_name=_(u'Start date'))
    deal_end_date = models.DateTimeField(blank=True, null=True, verbose_name=_(u'End date'))
    deal_conditions = models.TextField(blank=True, verbose_name=_(u'Conditions'))
    #~ extra info
    deal_data = JSONField(blank=True, verbose_name=_(u'Extra data (json format)'))
    
    class Meta:
        abstract = True


class Brand(MetaBaseModel, MetaBaseNameModel, MetaBaseStatusModel, MetaBaseUniqueSlugModel, Deal):
    image = models.ImageField(blank=True, upload_to='brands', verbose_name=_(u'Image'))
    
    class Meta:
        verbose_name=_(u'Brand')
        verbose_name_plural = _(u'Brands')
        ordering = ['name']

    def __unicode__(self):
        return unicode(self.name)
    

class Category(MPTTModel, MetaBaseModel, MetaBaseNameModel, MetaBaseStatusModel, MetaBaseUniqueSlugModel, Deal):
    parent = TreeForeignKey('self', null=True, blank=True, related_name=u'children', verbose_name=_(u'Parent category'))
    image = models.ImageField(null=True, upload_to='categories', verbose_name=_(u"Navigation image"))
    template_name = models.CharField(max_length=60, choices=CATEGORY_TEMPLATE_NAMES, default=CATEGORY_TEMPLATE_NAMES[0][0], verbose_name=_(u'Template'))
    description = models.TextField(blank=True, verbose_name=_(u'Description'))
    
    
    class Meta:
        verbose_name=_(u'Category')
        verbose_name_plural = _(u'Categories')

    def __unicode__(self):
        return unicode(self.name)


class Product(MetaBaseModel, MetaBaseNameModel, MetaBaseStatusModel, MetaBaseUniqueSlugModel, Deal):
    #~ base content
    short_description = models.TextField(blank=True, verbose_name=_(u'Short description'))
    description = models.TextField(blank=True, verbose_name=_(u'Long description'))
    upc = models.CharField(null=True, unique=True, max_length=30, verbose_name=_(u'Universal Product Code'))
    navimage = models.ImageField(null=True, upload_to='products/nav/', verbose_name=_(u'Navigation image'))
    #~ external keys
    brand = models.ForeignKey(Brand, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_(u'Brand'))
    category = TreeForeignKey(Category, verbose_name=_(u'Category'))
    #~ prices
    price = models.FloatField(null=True, blank=True, verbose_name=_(u'Price'))
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
    #~ slideshow options
    slideshow_width = models.PositiveSmallIntegerField(null=True, blank=True, default=800, verbose_name=_(u'Width'))
    slideshow_height = models.PositiveSmallIntegerField(null=True, blank=True, default=600, verbose_name=_(u'Height'))
    slideshow_type = models.CharField(max_length=150, choices=SLIDESHOW_TYPES, default=SLIDESHOW_TYPES[2][0], verbose_name=_(u'Slideshow type'))
    #~ template choice option
    template_name = models.CharField(max_length=60, choices=PRODUCT_TEMPLATE_NAMES, default=PRODUCT_TEMPLATE_NAMES[0][0], verbose_name=_(u'Template'))
    #~ extra info
    extra = JSONField(blank=True, verbose_name=_(u'Extra infos'))
    
    class Meta:
        verbose_name=_(u'Product')
        verbose_name_plural =_( u'Products')
        ordering = ('name','created')

    def __unicode__(self):
        return unicode(self.name)
    
    def print_caracteristics(self):
        """
        Used for debug
        """
        print 'Carac 1: '+str(self.carac1)
        print 'Carac 2: '+str(self.carac2)
        print 'Carac 3: '+str(self.carac3)
        print 'Carac 4: '+str(self.carac4)
        print 'Carac 5: '+str(self.carac5)
        print 'Int carac 1: '+str(self.int_carac1)
        print 'Int carac 1 name: '+str(self.int_carac1_name)
        print 'Int carac 2: '+str(self.int_carac2)
        print 'Int carac 2 name: '+str(self.int_carac2_name)
        print 'Int carac 3: '+str(self.int_carac3)
        print 'Int carac 3 name: '+str(self.int_carac3_name)
        return
    
    def reset_caracteristics(self):
        """
        Used for debug
        """
        self.carac1 = ''
        self.carac2 = ''
        self.carac3 = ''
        self.carac4 = ''
        self.carac5 = ''
        self.int_carac1 = None
        self.int_carac2 = None
        self.int_carac3 = None
        self.int_carac1_name = ''
        self.int_carac2_name = ''
        self.int_carac3_name = ''
        self.save()
        return
    
    
class ProductImage(MetaBaseModel, MetaBaseStatusModel, MetaBaseOrderedModel):
    image = models.ImageField(upload_to='products', verbose_name=_(u'Image'))
    #~ external key
    product = models.ForeignKey(Product, related_name="images", verbose_name=_(u'Product'))
    
    class Meta:
        verbose_name=_(u'Product image')
        verbose_name_plural = _(u'Product images')

    def __unicode__(self):
        return unicode(self.image.url)
    

class CategoryCaracteristic(MetaBaseModel, MetaBaseNameModel, MetaBaseUniqueSlugModel, MetaBaseOrderedModel):
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
            slug = unicode.strip(splited[0])
            name = unicode.strip(splited[1])
            choices[name] = slug+';'+ftype
        return choices
    
    def get_value_name(self, value, ftype):
        if ftype == 'choices':
            for choice in self.choices.split('\n'):
                splited = choice.split('>')
                slug = unicode.strip(splited[0])
                val = unicode.strip(splited[1])
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


class ProductCaracteristic(MetaBaseModel, MetaBaseNameModel):
    product = models.ForeignKey(Product, related_name="caracteristics", verbose_name=_(u'Product'))
    #category_caracteristic = models.ForeignKey(CategoryCaracteristic, related_name="+", verbose_name=_(u'Category caracteristic'))
    type = models.CharField(max_length=255, verbose_name=_(u'Type'))
    type_name = models.CharField(max_length=255, verbose_name=_(u'Type name'))
    value = models.CharField(max_length=255, verbose_name=_(u'Value'))
    value_name = models.CharField(max_length=255, verbose_name=_(u'Value name'))

    class Meta:
        verbose_name=_(u'Product caracteristic')
        verbose_name_plural =_( u'Product caracteristics')
        ordering = ('name', 'created')
        unique_together = ('name', 'product')

    def __unicode__(self):
        return unicode(self.name)
    
    def format_value(self, ftype):
        return self.name+':'+unicode.strip(self.value)+';'+ftype
    
    def save(self, *args, **kwargs):
        #print 'save product ----------------'
        if self.pk:
            product = self.product
            carac_type = CategoryCaracteristic.objects.filter(slug=self.name).select_related('category')[0]
            #if product.category <> carac_type.category:
            #    print "Wrong carac"
            ftype = carac_type.type
            self.value_name = carac_type.get_value_name(self.value, ftype)
            val = self.format_value(ftype)
            field = False
            if ftype in ['choices', 'boolean']:
                #print self.name+' / '+str(product.carac1)+' > '+str(is_name_in_field(self.name, product.carac1))
                if product.carac1 == '' or is_name_in_field(self.name, product.carac1):
                    product.carac1 = val
                    field = True
                if field is False and product.carac2 == '' or is_name_in_field(self.name, product.carac2):
                    product.carac2 = val
                    field = True
                if field is False and product.carac3 == '' or is_name_in_field(self.name, product.carac3):
                    product.carac3 = val
                    field = True
                if field is False and product.carac4 == '' or is_name_in_field(self.name, product.carac4):
                    product.carac4 = val
                    field = True
                if field is False and product.carac5 == '' or is_name_in_field(self.name, product.carac5):
                    product.carac5 = val
            field = False
            if ftype == 'int':
                if product.int_carac1 is None or product.int_carac1_name == self.name:
                    product.int_carac1 = int(self.value)
                    product.int_carac1_name = self.name
                    field = True
                if field is False and product.int_carac2 is None or product.int_carac2_name == self.name:
                    product.int_carac2 = int(self.value)
                    product.int_carac2_name = self.name
                    field = True
                if field is False and product.int_carac3 is None or product.int_carac3_name == self.name:
                    product.int_carac3 = int(self.value)
                    product.int_carac3_name = self.name
            product.save()
        super(ProductCaracteristic, self).save()
    
    

    
            
        
        


