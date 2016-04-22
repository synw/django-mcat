# -*- coding: utf-8 -*-

import tempfile
from collections import OrderedDict
from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from autofixture import AutoFixture
from mqueue.models import MEvent
from mcat.models import Brand, Category, Product, ProductImage, ProductCaracteristic, CategoryCaracteristic
from mcat.conf import USE_PRICES


class McatBrandTest(TestCase):
    
    def create_brand(self):
        fixture = AutoFixture(Brand, field_values={'slug':'obj-slug','status':0})
        fixture.create(1)
        self.obj = Brand.objects.get(slug='obj-slug')
        return self.obj
        
    def test_brand_creation(self):
        brand = self.create_brand()
        self.assertTrue(isinstance(brand, Brand))
        self.assertEqual(brand.slug, self.obj.slug)
        self.assertEqual(brand.name, self.obj.name)
        self.assertEqual(brand.status, 0)
        self.assertEqual(brand.image, self.obj.image)
        self.assertEqual(brand.__unicode__(), self.obj.name)
        return
    

class McatCategoryTest(TestCase):
    
    def create_obj(self, slug="obj_slug", name="Obj name", status=0, filters_position='side', parent=None):
        self.image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        obj = Category.objects.create(slug=slug, name=name, image=self.image, status=status, parent=parent, filters_position=filters_position)
        return obj
        
    def test_obj_creation(self):
        parent_obj = self.create_obj(slug='parent-obj')
        obj = self.create_obj(parent=parent_obj)
        self.assertTrue(isinstance(obj, Category))
        self.assertEqual(obj.slug, 'obj_slug')
        self.assertEqual(obj.name, "Obj name")
        self.assertEqual(obj.status, 0)
        self.assertEqual(obj.filters_position, 'side')
        self.assertEqual(obj.image, self.image)
        self.assertEqual(obj.__unicode__(), obj.name)
        self.assertTrue(obj.parent, parent_obj)
        return

   
class McatProductTest(TestCase):
    
    def create_obj(self):
        fixture = AutoFixture(Product, field_values={'slug':'obj-slug','status':0, 'price':100.0}, generate_fk=True)
        fixture.create(1)
        self.obj = Product.objects.get(slug='obj-slug')
        return self.obj
    
    @override_settings(MCAT_USE_PRICES = True, MCAT_PRICES_AS_INTEGER = True)     
    def test_obj_creation(self):
        obj = self.create_obj()
        self.assertTrue(isinstance(obj, Product))
        self.assertEqual(obj.slug, self.obj.slug)
        self.assertEqual(obj.name, self.obj.name)
        self.assertEqual(obj.status, 0)
        self.assertEqual(obj.navimage, self.obj.navimage)
        self.assertEqual(obj.brand, self.obj.brand)
        self.assertEqual(obj.category, self.obj.category)
        self.assertEqual(obj.price, self.obj.price)
        self.assertEqual(obj.discounted_price, self.obj.discounted_price)
        self.assertEqual(obj.discounted_percentage, self.obj.discounted_percentage)
        self.assertEqual(obj.carac1, self.obj.carac1)
        self.assertEqual(obj.carac2, self.obj.carac2)
        self.assertEqual(obj.carac3, self.obj.carac3)
        self.assertEqual(obj.carac4, self.obj.carac4)
        self.assertEqual(obj.carac5, self.obj.carac5)
        self.assertEqual(obj.int_carac1, self.obj.int_carac1)
        self.assertEqual(obj.int_carac2, self.obj.int_carac2)
        self.assertEqual(obj.int_carac3, self.obj.int_carac3)
        self.assertEqual(obj.int_carac1_name, self.obj.int_carac1_name)
        self.assertEqual(obj.int_carac2_name, self.obj.int_carac2_name)
        self.assertEqual(obj.int_carac3_name, self.obj.int_carac3_name)
        self.assertEqual(obj.__unicode__(), obj.name)
        #print 'UP TEST : '+str(settings.MCAT_USE_PRICES)
        if USE_PRICES is True:
            self.assertEqual(obj.get_price(), 100)
        else:
            self.assertIsNone(obj.get_price())
        return


class McatProductImageTest(TestCase):
    
    def create_obj(self):
        fixture = AutoFixture(ProductImage, field_values={'status':0}, generate_fk=True)
        fixture.create(1)
        self.obj = ProductImage.objects.get(pk=1)
        return self.obj
      
    def test_obj_creation(self):
        obj = self.create_obj()
        self.assertTrue(isinstance(obj, ProductImage))
        self.assertEqual(obj.status, 0)
        self.assertEqual(obj.order, self.obj.order)
        self.assertEqual(obj.product, self.obj.product)
        self.assertEqual(obj.image, self.obj.image)
        self.assertEqual(obj.__unicode__(), obj.image.url)
        return

choices = '-10 > Less than 10\n10_20 > 10 to 20\n+20 > More than 20 '
class McatProductCaracteristicTest(TestCase):
    
    def create_obj(self, product, ftype, value):
        fixture = AutoFixture(ProductCaracteristic, field_values={'name':'carac1', 'product':product})
        fixture.create(1)
        self.obj = ProductCaracteristic.objects.get(pk=1)
        self.obj.value = value
        self.obj.type = ftype
        self.obj.save()
        return self.obj
    
    def create_category_caracteristic(self, ftype, choices=choices, name='Carac name'):
        fixture = AutoFixture(Category, field_values={'slug':'cat-slug'})
        fixture.create(1)
        self.category = Category.objects.get(slug='cat-slug')
        fixture = AutoFixture(CategoryCaracteristic, field_values={
                                                                   'name':name,
                                                                   'category':self.category, 
                                                                   'type':ftype,
                                                                   'slug':'carac1',
                                                                   'unit':'cm',
                                                                   'choices':choices
                                                                   }
                              )
        fixture.create(1)
    
    def create_product(self, ftype, slug='obj-slug', carac1='', carac2='', carac3='', carac4='', carac5='', int_carac1=None, int_carac2=None, int_carac3=None, int_carac1_name='', int_carac2_name='', int_carac3_name=''):
        self.create_category_caracteristic(ftype=ftype)
        fixture = AutoFixture(Product, field_values={'slug':slug,
                                                     'status':0, 
                                                     'category':self.category,
                                                     'carac1':carac1,
                                                     'carac2':carac2,
                                                     'carac3':carac3,
                                                     'carac4':carac4,
                                                     'carac5':carac5,
                                                     'int_carac1':int_carac1,
                                                     'int_carac2':int_carac2,
                                                     'int_carac3':int_carac3,
                                                     'int_carac1_name':int_carac1_name,
                                                     'int_carac2_name':int_carac2_name,
                                                     'int_carac3_name':int_carac3_name,
                                                     }
                              )
        fixture.create(1)
        self.product = Product.objects.get(slug=slug)
        return self.product

    def test_obj_creation(self):
        obj = self.create_obj(product=self.create_product('p'), ftype='int', value=u'15')
        self.assertTrue(isinstance(obj, ProductCaracteristic))
        self.assertEqual(obj.name, self.obj.name)
        self.assertEqual(obj.product, self.obj.product)
        self.assertEqual(obj.type, self.obj.type)
        self.assertEqual(obj.type_name, self.obj.type_name)
        self.assertEqual(obj.value, self.obj.value)
        self.assertEqual(obj.value_name, self.obj.value_name)
        self.assertEqual(obj.__unicode__(), obj.name)
        return
    
    def test_save_int_caracteristic1(self):
        product = self.create_product(slug='p1', ftype='int')
        obj = self.create_obj(product=product, ftype='int', value=u'15')
        carac = CategoryCaracteristic.objects.get(category=product.category, name='Carac name')
        obj.save()
        product = Product.objects.get(slug='p1')
        self.assertEqual(product.int_carac1, int(obj.value))
        self.assertEqual(product.int_carac1_name, obj.name)
        self.assertEqual(obj.value, str(product.int_carac1))
        self.assertEqual(obj.type, carac.type)
        return
    
    
    def test_save_int_caracteristic2(self):
        product = self.create_product(slug='p2', ftype='int', int_carac1=10, int_carac1_name='carac')
        obj = self.create_obj(product=product, ftype='int', value=u'15')
        carac = CategoryCaracteristic.objects.get(category=product.category, name='Carac name')
        obj.save()
        product = Product.objects.get(slug='p2')
        self.assertEqual(product.int_carac2, int(obj.value))
        self.assertEqual(product.int_carac2_name, obj.name)
        self.assertEqual(obj.value, str(product.int_carac2))
        self.assertEqual(obj.type, carac.type)
        return
    
    def test_save_int_caracteristic3(self):
        product = self.create_product(slug='p3', ftype='int', int_carac1=10, int_carac1_name='carac', int_carac2=10, int_carac2_name='carac2')
        obj = self.create_obj(product=product, ftype='int', value=u'15')
        carac = CategoryCaracteristic.objects.get(category=product.category, name='Carac name')
        obj.save()
        product = Product.objects.get(slug='p3')
        self.assertEqual(product.int_carac3, int(obj.value))
        self.assertEqual(product.int_carac3_name, obj.name)
        self.assertEqual(obj.value, str(product.int_carac3))
        self.assertEqual(obj.type, carac.type)
        return
    
    def test_update_int_caracteristic(self):
        product = self.create_product(slug='p', ftype='int', int_carac1=10, int_carac1_name='carac1')
        obj = self.create_obj(product=product, ftype='int', value=u'15')
        carac = CategoryCaracteristic.objects.get(category=product.category, name='Carac name')
        obj.save()
        product = Product.objects.get(slug='p')
        self.assertEqual(product.int_carac1, int(obj.value))
        self.assertEqual(product.int_carac1_name, obj.name)
        self.assertEqual(obj.value, str(product.int_carac1))
        self.assertEqual(obj.type, carac.type)
        return
    

    def test_save_boolean_caracteristic1(self):
        product = self.create_product(slug='p4', ftype='boolean')
        obj = self.create_obj(product=product, ftype='boolean', value=u'1')
        carac = CategoryCaracteristic.objects.get(category=product.category, name='Carac name')
        obj.save()
        product = Product.objects.get(slug='p4')
        val = obj.format_value(carac.type)
        self.assertEqual(product.carac1, val)
        self.assertEqual(obj.type, carac.type)
        self.assertEqual(obj.value, u'1')
        return
    
    def test_save_boolean_caracteristic2(self):
        product = self.create_product(slug='p4', ftype='boolean', carac1='c')
        obj = self.create_obj(product=product, ftype='boolean', value=u'1')
        carac = CategoryCaracteristic.objects.get(category=product.category, name='Carac name')
        obj.save()
        product = Product.objects.get(slug='p4')
        val = obj.format_value(carac.type)
        self.assertEqual(product.carac2, val)
        self.assertEqual(obj.type, carac.type)
        self.assertEqual(obj.value, u'1')
        return
  
    def test_save_boolean_caracteristic3(self):
        product = self.create_product(slug='p4', ftype='boolean', carac1='c', carac2='c')
        obj = self.create_obj(product=product, ftype='boolean', value=u'1')
        carac = CategoryCaracteristic.objects.get(category=product.category, name='Carac name')
        obj.save()
        product = Product.objects.get(slug='p4')
        val = obj.format_value(carac.type)
        self.assertEqual(product.carac3, val)
        self.assertEqual(obj.type, carac.type)
        self.assertEqual(obj.value, u'1')
        return
    
    def test_save_boolean_caracteristic4(self):
        product = self.create_product(slug='p5', ftype='boolean', carac1='c', carac2='c', carac3='c')
        obj = self.create_obj(product=product, ftype='boolean', value=u'1')
        carac = CategoryCaracteristic.objects.get(category=product.category, name='Carac name')
        obj.save()
        product = Product.objects.get(slug='p5')
        val = obj.format_value(carac.type)
        self.assertEqual(product.carac4, val)
        self.assertEqual(obj.type, carac.type)
        self.assertEqual(obj.value, u'1')
        return
    
    def test_save_boolean_caracteristic5(self):
        product = self.create_product(slug='p6', ftype='boolean', carac1='c', carac2='c', carac3='c', carac4='c')
        obj = self.create_obj(product=product, ftype='boolean', value=u'1')
        carac = CategoryCaracteristic.objects.get(category=product.category, name='Carac name')
        obj.save()
        product = Product.objects.get(slug='p6')
        val = obj.format_value(carac.type)
        self.assertEqual(product.carac5, val)
        self.assertEqual(obj.type, carac.type)
        self.assertEqual(obj.value, u'1')
        return
    
    def test_update_boolean_caracteristic1(self):
        product = self.create_product(slug='p5', ftype='boolean', carac1='carac1:0;boolean' )
        obj = self.create_obj(product=product, ftype='boolean', value=u'1')
        carac = CategoryCaracteristic.objects.get(category=product.category, name='Carac name')
        obj.save()
        product = Product.objects.get(slug='p5')
        val = obj.format_value(carac.type)
        self.assertEqual(product.carac1, val)
        self.assertEqual(obj.type, carac.type)
        self.assertEqual(obj.value, u'1')
        return
    
    def test_format_value(self):
        ftype = 'boolean'
        product = self.create_product(slug='p6', ftype='boolean', carac1='carac1:1;boolean')
        obj = self.create_obj(product=product, ftype='boolean', value=u'1')
        obj.save()
        self.assertEqual(product.carac1, obj.format_value(ftype))
        return


choices = 'choice1 > Choice 1\nchoice2 > Choice 2'
class McatCategoryCaracteristicTest(TestCase):
    
    def create_obj(self, slug='cat1', category=None, name='carac_name', ftype='int', unit='cm'):
        fixture = AutoFixture(Category, field_values={'slug':'cat1'})
        fixture.create(1)
        if category is None:
            category  = Category.objects.get(slug=slug)
        fixture = AutoFixture(CategoryCaracteristic, field_values={
                                                                   'name':name,
                                                                   'category':category,
                                                                   'type':ftype,
                                                                   'unit':unit,
                                                                   'choices':choices
                                                                   }
                              )
        fixture.create(1)
        self.obj = CategoryCaracteristic.objects.get(pk=1)
        self.obj.type = ftype
        self.obj.save()
        self.category = category
        return self.obj
    
    def test_object_creation(self):
        obj = self.create_obj()
        self.assertTrue(isinstance(obj, CategoryCaracteristic))
        self.assertEqual(obj.name, 'carac_name')
        self.assertEqual(obj.category, self.category)
        self.assertEqual(obj.type, 'int')
        self.assertEqual(obj.unit, 'cm')
        self.assertEqual(obj.__unicode__(), obj.name)
        return
    
    def test_get_choices(self):
        obj = self.create_obj(ftype='choices')
        choices_dict = OrderedDict()
        choices_dict['Choice 1'] = 'choice1;c'
        choices_dict['Choice 2'] = 'choice2;c'
        self.assertEqual(obj.get_choices(), choices_dict)
        return
    """
    def test_get_value_name(self):
        obj = self.create_obj(ftype='boolean')
        self.assertEqual(obj.get_value_name(obj.value, 'boolean'), str(obj.value))
        obj = self.create_obj(ftype='int', unit='meters')
        self.assertEqual(obj.get_value_name(obj.value, 'int'), obj.value+'&nbsp;meters')
        return
    """



