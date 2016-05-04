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
    
    def create_category_caracteristic(self, slug="slug", category=None, ftype='boolean', choices=choices, name='carac_name'):
        if category is None:
            category = self.create_category()
        fixture = AutoFixture(CategoryCaracteristic, field_values={
                                                                   'slug':slug,
                                                                   'category':category,
                                                                   'choices':choices,
                                                                   'name':name,
                                                                   'type':ftype,
                                                                   }
                              )
        return fixture.create(1)[0]
    
    def create_product(self, ftype='boolean', category=None, category_carac=True, name='product', slug='obj-slug', carac1='', carac2='', carac3='', carac4='', carac5='', int_carac1=None, int_carac2=None, int_carac3=None, int_carac1_name='', int_carac2_name='', int_carac3_name=''):
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

    def create_obj(self, product, ftype, value, name, type_name='', value_name=''):
        obj = ProductCaracteristic.objects.create(name=name, product=product, value=value, type=ftype, value_name=value_name, type_name=type_name)
        return obj
    

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

    def test_save_int_caracteristics(self):
        category = self.create_category()
        cat_carac1 = self.create_category_caracteristic(slug="cslug1", category=category, ftype='boolean', choices='', name='carac_name1')
        cat_carac2 = self.create_category_caracteristic(slug="cslug2", category=category, ftype='boolean', choices='', name='carac_name2')
        cat_carac3 = self.create_category_caracteristic(slug="cslug3", category=category, ftype='boolean', choices='', name='carac_name3')
        cat_carac4 = self.create_category_caracteristic(slug="cslug4", category=category, ftype='boolean', choices='', name='carac_name4')
        cat_carac5 = self.create_category_caracteristic(slug="cslug5", category=category, ftype='choices', choices=choices, name='carac_name5')
        int_cat_carac1 = self.create_category_caracteristic(slug="cslug6", category=category, ftype='int', choices='', name='carac_name6')
        int_cat_carac2 = self.create_category_caracteristic(slug="cslug7", category=category, ftype='int', choices='', name='carac_name7')
        int_cat_carac3 = self.create_category_caracteristic(slug="cslug8", category=category, ftype='int', choices='', name='carac_name8')
        # the product is supposed to autogenerate his own product caracteristics on creation based on category caracteristics
        product = self.create_product(category=category, slug='p44')
        #~ int carac 1
        pcarac = ProductCaracteristic.objects.get(name=int_cat_carac1.slug, product=product)
        pcarac.value = u'1'
        pcarac.type = u'int'
        pcarac.unit = u'm'
        pcarac.save()
        self.assertEqual(pcarac.value, u'1')
        self.assertEqual(pcarac.name, int_cat_carac1.slug)
        self.assertEqual(pcarac.type, 'int')
        self.assertEqual(pcarac.value_name, int_cat_carac1.get_value_name(pcarac.value, pcarac.type))
        #~ check if product has recorded the values
        product = Product.objects.get(slug='p44')
        self.assertEqual(product.int_carac1, int(pcarac.value))
        self.assertEqual(product.int_carac1_name, pcarac.name)
        # int carac 2
        pcarac = ProductCaracteristic.objects.get(name=int_cat_carac2.slug, product=product)
        pcarac.value = u'1'
        pcarac.type = u'int'
        pcarac.unit = u'm'
        pcarac.save()
        self.assertEqual(pcarac.value, u'1')
        self.assertEqual(pcarac.name, int_cat_carac2.slug)
        self.assertEqual(pcarac.type, 'int')
        self.assertEqual(pcarac.value_name, int_cat_carac2.get_value_name(pcarac.value, pcarac.type))
        #~ check if product has recorded the values
        product = Product.objects.get(slug='p44')
        self.assertEqual(product.int_carac2, int(pcarac.value))
        self.assertEqual(product.int_carac2_name, pcarac.name)
        #~ int carac 3
        pcarac = ProductCaracteristic.objects.get(name=int_cat_carac3.slug, product=product)
        pcarac.value = u'1'
        pcarac.type = u'int'
        pcarac.unit = u'm'
        pcarac.save()
        self.assertEqual(pcarac.value, u'1')
        self.assertEqual(pcarac.name, int_cat_carac3.slug)
        self.assertEqual(pcarac.type, 'int')
        self.assertEqual(pcarac.value_name, int_cat_carac3.get_value_name(pcarac.value, pcarac.type))
        #~ check if product has recorded the values
        product = Product.objects.get(slug='p44')
        self.assertEqual(product.int_carac3, int(pcarac.value))
        self.assertEqual(product.int_carac3_name, pcarac.name)
        # carac 1
        pcarac = ProductCaracteristic.objects.get(name=cat_carac2.slug, product=product)
        pcarac.value = u'1'
        pcarac.type = cat_carac2.type
        pcarac.save()
        self.assertEqual(pcarac.value, u'1')
        self.assertEqual(pcarac.name, cat_carac2.slug)
        self.assertEqual(pcarac.type, 'boolean')
        self.assertEqual(pcarac.value_name, cat_carac2.get_value_name(pcarac.value, pcarac.type))
        return
        # carac 2
        pcarac = ProductCaracteristic.objects.get(name=cat_carac3.slug, product=product)
        pcarac.value = u'1'
        pcarac.type = cat_carac3.type
        pcarac.save()
        self.assertEqual(pcarac.value, u'1')
        self.assertEqual(pcarac.name, cat_carac3.slug)
        self.assertEqual(pcarac.type, 'boolean')
        self.assertEqual(pcarac.value_name, cat_carac3.get_value_name(pcarac.value, pcarac.type))
        return
        # carac 3
        pcarac = ProductCaracteristic.objects.get(name=cat_carac3.slug, product=product)
        pcarac.value = u'1'
        pcarac.type = cat_carac3.type
        pcarac.save()
        self.assertEqual(pcarac.value, u'1')
        self.assertEqual(pcarac.name, cat_carac3.slug)
        self.assertEqual(pcarac.type, 'boolean')
        self.assertEqual(pcarac.value_name, cat_carac3.get_value_name(pcarac.value, pcarac.type))
        return
        # carac 4
        pcarac = ProductCaracteristic.objects.get(name=cat_carac4.slug, product=product)
        pcarac.value = u'1'
        pcarac.type = cat_carac4.type
        pcarac.save()
        self.assertEqual(pcarac.value, u'1')
        self.assertEqual(pcarac.name, cat_carac4.slug)
        self.assertEqual(pcarac.type, 'boolean')
        self.assertEqual(pcarac.value_name, cat_carac4.get_value_name(pcarac.value, pcarac.type))
        return
        # carac 5
        pcarac = ProductCaracteristic.objects.get(name=cat_carac5.slug, product=product)
        pcarac.value = u'10_20'
        pcarac.type = cat_carac5.type
        pcarac.save()
        self.assertEqual(pcarac.value, u'10_20')
        self.assertEqual(pcarac.name, cat_carac5.slug)
        self.assertEqual(pcarac.type, 'choices')
        self.assertEqual(pcarac.value_name, cat_carac5.get_value_name(pcarac.value, pcarac.type))
        return

    def test_format_value(self):
        ftype = 'boolean'
        product = self.create_product(slug='p6', ftype='boolean', name='pc54', carac1='pc54:1;boolean')
        obj = self.create_obj(product=product, name="pc54", ftype='boolean', value=u'1')
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



