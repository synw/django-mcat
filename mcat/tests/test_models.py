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
    
    def create_obj(self, slug="obj_slug", name="Obj name", status=0, template_name='default', parent=None):
        self.image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        obj = Category.objects.create(slug=slug, name=name, image=self.image, status=status, parent=parent, template_name=template_name)
        return obj
        
    def test_obj_creation(self):
        parent_obj = self.create_obj(slug='parent-obj')
        obj = self.create_obj(parent=parent_obj)
        self.assertTrue(isinstance(obj, Category))
        self.assertEqual(obj.slug, 'obj_slug')
        self.assertEqual(obj.name, "Obj name")
        self.assertEqual(obj.status, 0)
        self.assertEqual(obj.template_name, 'default')
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
    
    def create_category(self, slug="obj_slug", name="Obj name", status=0, template_name='default', parent=None):
        self.image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        obj = Category.objects.create(slug=slug, name=name, image=self.image, status=status, parent=parent, template_name=template_name)
        return obj
    
    def create_obj(self, product, ftype, value, name='product_carac_name', type_name='', value_name=''):
        fixture = AutoFixture(ProductCaracteristic, field_values={
                                                                  'name':name, 
                                                                  'product':product, 
                                                                  'value':value, 
                                                                  'type':ftype,
                                                                  'type_name':type_name,
                                                                  'value_name':value_name,
                                                                  }
                              )
        obj = fixture.create(1)[0]
        return obj
    
    def create_category_caracteristic(self, slug="slug", category=None, ftype='boolean', choices=choices, name='carac_name'):
        if category is None:
            self.create_category()
        fixture = AutoFixture(CategoryCaracteristic, field_values={
                                                                   'slug':slug,
                                                                   'category':category,
                                                                   'choices':choices,
                                                                   'name':name,
                                                                   'type':ftype,
                                                                   }
                              )
        return fixture.create(1)[0]
    
    def create_product(self, ftype, category=None, category_carac=True, name='product', slug='obj-slug', carac1='', carac2='', carac3='', carac4='', carac5='', int_carac1=None, int_carac2=None, int_carac3=None, int_carac1_name='', int_carac2_name='', int_carac3_name=''):
        if category is None:
            category = self.create_category()
        if category_carac is True:
            category_carac = self.create_category_caracteristic(ftype=ftype, category=category)
        fixture = AutoFixture(Product, field_values={'slug':slug,
                                                     'name':name,
                                                     'status':0, 
                                                     'category':category,
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
        product = fixture.create(1)[0]
        return product

    def test_obj_creation(self):
        product = self.create_product('p')
        obj = self.create_obj(product=product, ftype='int', value=u'15', name='cname')
        self.assertTrue(isinstance(obj, ProductCaracteristic))
        self.assertEqual(obj.name, 'cname')
        self.assertEqual(obj.product, product)
        self.assertEqual(obj.type, 'int')
        self.assertEqual(obj.value, '15')
        #self.assertEqual(obj.type_name, self.obj.type_name)
        #self.assertEqual(obj.value_name, self.obj.value_name)
        self.assertEqual(obj.__unicode__(), 'cname')
        return
    
    def test_save_int_caracteristic1(self):
        category = self.create_category()
        cat_carac = self.create_category_caracteristic(slug="cslug1", category=category, ftype='int', choices='', name='carac_name')
        product = self.create_product(category_carac=False, category=category, slug='p44', ftype='int')
        obj = self.create_obj(product=product, ftype='int', name='cslug1', value=u'1')
        obj.save()
        self.assertEqual(product.int_carac1, int(obj.value))
        self.assertEqual(product.int_carac1_name, obj.name)
        self.assertEqual(obj.value, str(product.int_carac1))
        self.assertEqual(obj.type, cat_carac.type)
        return
    
    
    def test_save_int_caracteristic2(self):
        category = self.create_category()
        cat_carac = self.create_category_caracteristic(slug="cslug1", category=category, ftype='int', choices='', name='carac_name')
        product = self.create_product(category_carac=False, category=category, slug='p44', ftype='int')
        obj = self.create_obj(product=product, ftype='int', name='cslug1', value=u'1')
        product.int_carac1 = 1
        obj.save()
        self.assertEqual(product.int_carac2, int(obj.value))
        self.assertEqual(product.int_carac2_name, obj.name)
        self.assertEqual(obj.value, str(product.int_carac2))
        self.assertEqual(obj.type, cat_carac.type)
        return
    
    def test_save_int_caracteristic3(self):
        category = self.create_category()
        cat_carac = self.create_category_caracteristic(slug="cslug1", category=category, ftype='int', choices='', name='carac_name')
        product = self.create_product(category_carac=False, category=category, slug='p44', ftype='int')
        obj = self.create_obj(product=product, ftype='int', name='cslug1', value=u'1')
        product.int_carac1 = 1
        product.int_carac2 = 1
        obj.save()
        self.assertEqual(product.int_carac3, int(obj.value))
        self.assertEqual(product.int_carac3_name, obj.name)
        self.assertEqual(obj.value, str(product.int_carac3))
        self.assertEqual(obj.type, cat_carac.type)
        return
    
    def test_update_int_caracteristic(self):
        category = self.create_category()
        cat_carac = self.create_category_caracteristic(slug="cslug1", category=category, ftype='int', choices='', name='carac_name')
        product = self.create_product(category_carac=False, category=category, slug='p44', ftype='int')
        obj = self.create_obj(product=product, ftype='int', name='cslug1', value=u'1')
        obj.value = u'2'
        obj.save()
        self.assertEqual(product.int_carac1, int(obj.value))
        self.assertEqual(product.int_carac1_name, obj.name)
        self.assertEqual(obj.value, str(product.int_carac1))
        self.assertEqual(obj.type, cat_carac.type)
        return
    

    def test_save_boolean_caracteristic1(self):
        category = self.create_category()
        cat_carac = self.create_category_caracteristic(slug="cslug1", category=category, ftype='boolean', choices='', name='carac_name')
        product = self.create_product(category_carac=False, category=category, slug='p44', ftype='boolean')
        obj = self.create_obj(product=product, ftype='boolean', name='cslug1', value=u'1')
        #~ save it to fill product carac values on Product model
        obj.save()
        val = obj.format_value(obj.type)
        self.assertEqual(product.carac1, val)
        self.assertEqual(obj.type, cat_carac.type)
        self.assertEqual(obj.value, u'1')
        return
    
    def test_save_boolean_caracteristic2(self):
        category = self.create_category()
        cat_carac = self.create_category_caracteristic(slug="cslug1", category=category, ftype='boolean', choices='', name='carac_name')
        product = self.create_product(category_carac=False, category=category, slug='p4', ftype='boolean')
        product.carac1='x'
        obj = self.create_obj(product=product, ftype='boolean', name='cslug1', value=u'1')
        #carac = CategoryCaracteristic.objects.get(category=product.category)
        obj.save()
        product = Product.objects.get(slug='p4')
        val = obj.format_value(obj.type)
        self.assertEqual(product.carac2, val)
        self.assertEqual(obj.type, 'boolean')
        self.assertEqual(obj.value, u'1')
        return
  
    def test_save_boolean_caracteristic3(self):
        category = self.create_category()
        cat_carac = self.create_category_caracteristic(slug="cslug1", category=category, ftype='boolean', choices='', name='carac_name')
        product = self.create_product(category_carac=False, category=category, slug='p4', ftype='boolean')
        product.carac1='x'
        product.carac2='x'
        obj = self.create_obj(product=product, ftype='boolean', name='cslug1', value=u'1')
        obj.save()
        product = Product.objects.get(slug='p4')
        val = obj.format_value(obj.type)
        self.assertEqual(product.carac3, val)
        self.assertEqual(obj.type, cat_carac.type)
        self.assertEqual(obj.value, u'1')
        return
    
    def test_save_boolean_caracteristic4(self):
        category = self.create_category()
        cat_carac = self.create_category_caracteristic(slug="cslug1", category=category, ftype='boolean', choices='', name='carac_name')
        product = self.create_product(category_carac=False, category=category, slug='p4', ftype='boolean')
        product.carac1='x'
        product.carac2='x'
        product.carac3='x'
        obj = self.create_obj(product=product, ftype='boolean', name='cslug1', value=u'1')
        obj.save()
        val = obj.format_value(obj.type)
        self.assertEqual(product.carac4, val)
        self.assertEqual(obj.type, cat_carac.type)
        self.assertEqual(obj.value, u'1')
        return
    
    def test_save_boolean_caracteristic5(self):
        category = self.create_category()
        cat_carac = self.create_category_caracteristic(slug="cslug1", category=category, ftype='boolean', choices='', name='carac_name')
        product = self.create_product(category_carac=False, category=category, slug='p4', ftype='boolean')
        product.carac1='x'
        product.carac2='x'
        product.carac3='x'
        product.carac4='x'
        obj = self.create_obj(product=product, ftype='boolean', name='cslug1', value=u'1')
        obj.save()
        val = obj.format_value(obj.type)
        self.assertEqual(product.carac5, val)
        self.assertEqual(obj.type, cat_carac.type)
        self.assertEqual(obj.value, u'1')
        return
    
    def test_update_boolean_caracteristic1(self):
        category = self.create_category()
        cat_carac = self.create_category_caracteristic(slug="cslug1", category=category, ftype='boolean', choices='', name='carac_name')
        product = self.create_product(category_carac=False, category=category, slug='p4', ftype='boolean')
        obj = self.create_obj(product=product, ftype='boolean', name='cslug1', value=u'1')
        obj.carac1 = 1
        obj.save()
        val = obj.format_value(obj.type)
        self.assertEqual(product.carac1, val)
        self.assertEqual(obj.type, cat_carac.type)
        self.assertEqual(obj.value, u'1')
        return
    
    def test_format_value(self):
        ftype = 'boolean'
        product = self.create_product(slug='p6', ftype='boolean', name='product_carac_name', carac1='product_carac_name:1;boolean')
        obj = self.create_obj(product=product, ftype='boolean', value=u'1')
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



