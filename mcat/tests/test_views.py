# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from django.test import TestCase
from autofixture import AutoFixture
from mcat.models import Category, Product, CategoryCaracteristic, ProductCaracteristic


#@override_settings(DEBUG=True)
class CategoryViewsTest(TestCase):
    
    #~ fixtures generators
    
    def create_categories(self, num):
        fixture = AutoFixture(Category, generate_fk=True)
        fixture.create(num)
        return
    
    def create_category(self, slug='obj_slug'):
        fixture = AutoFixture(Category, generate_fk=True, field_values={'slug':slug, 'filters_position':'side'})
        fixture.create(1)
        return
    
    def create_products(self, category):
        fixture = AutoFixture(Product, field_values={'category':category})
        fixture.create(3)
        return
    
    def create_product(self, category):
        fixture = AutoFixture(Product, field_values={'slug':'obj-slug','status':0, 'price':100.0, 'category':category}, generate_fk=True)
        fixture.create(1)
        obj = Product.objects.get(slug='obj-slug')
        return obj
    
    def create_category_caracteristic(self, slug='cat1', category=None, name='carac_name', ftype='int', unit='cm', choices = 'choice1 > Choice 1\nchoice2 > Choice 2'):
        if category is None:
            fixture = AutoFixture(Category, field_values={'slug':slug})
            fixture.create(1)
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
        obj = CategoryCaracteristic.objects.get(pk=1)
        obj.type = ftype
        obj.save()
        return obj
    
    def create_product_caracteristic(self, product, ftype, name, value):
        fixture = AutoFixture(ProductCaracteristic, field_values={'name':name, 
                                                                  'product':product,
                                                                  'ftype':ftype,
                                                                  'value':value
                                                                  }
                              )
        fixture.create(1)
        obj = ProductCaracteristic.objects.get(pk=1)
        obj.value = value
        obj.type = ftype
        obj.save()
        return obj
    
    #~ views tests
    
    def test_CategoryHomeView(self):
        self.create_categories(3)
        response = self.client.get(reverse('category-home'))
        categories = Category.objects.filter(level__lte=0, status=0)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['categories']), list(categories))
        self.assertEqual(response.context['num_categories'], len(categories))
        self.assertTemplateUsed(response, 'mcat/categories/index.html')
        return

    def test_CategoryView(self):
        self.create_category(slug='cat1')
        category = Category.objects.get(slug='cat1')
        last_level=category.level+1
        categories = category.get_descendants().filter(level__lte=last_level, status=0)
        ancestors = category.get_ancestors()
        response = self.client.get(reverse('category-list', kwargs={'slug':'cat1'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['categories']), list(categories))
        self.assertEqual(response.context['num_categories'], len(categories))
        self.assertEqual(response.context['current_category'], category)
        self.assertEqual(list(response.context['ancestors']), list(ancestors))
        self.assertTemplateUsed(response, 'mcat/categories/browse.html')
        return

    def test_ProductsInCategoryView(self):
        self.create_category(slug='cat2')
        category = Category.objects.filter(slug='cat2').prefetch_related('generic_caracteristics')[0]
        last_level=category.level+1
        categories = category.get_descendants().filter(level__lte=last_level)
        self.create_products(category=category)
        products = Product.objects.filter(category=category)
        response = self.client.get(reverse('product-list', kwargs={'slug':category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mcat/products/index.html')
        self.assertEqual(list(response.context['products']), list(products))
        self.assertEqual(response.context['category'], category)
        self.assertEqual(list(response.context['categories']), list(categories))
        self.assertEqual(response.context['num_categories'], len(categories))
        self.assertEqual(response.context['num_products'], len(products))
        self.assertTrue(response.context['use_filters'])
        self.assertFalse('disable_breadcrumbs' in response.context)
        self.assertEqual(response.context['filters_position'], 'side')
        self.assertEqual(list(response.context['ancestors']), list(category.get_ancestors()))
        self.assertEqual(list(response.context['caracteristics']), list(category.generic_caracteristics.all()))
        #~ filters tests
        choices = '-10 > Less than 10\n10_20 > 10 to 20\n+20 > More than 20'
        catcarac1 = self.create_category_caracteristic(category=category, slug='catcarac1', name='carac_name', ftype='int', unit='cm', choices=choices)
        choices = 'choice1 > Choice 1\nchoice2 > Choice 2'
        catcarac2 = self.create_category_caracteristic(category=category, slug='catcarac2', name='carac_name', ftype='choices', choices=choices)
        catcarac3 = self.create_category_caracteristic(category=category, slug='catcarac3', name='carac_name', ftype='boolean')
        product = self.create_product(category=category)
        #productcarac1 = self.create_product_caracteristic(product, ftype='int', name='int_carac', value='10_20', unit='cm')
        productcarac1 = self.create_product_caracteristic(product, ftype='boolean', name='boolean_carac', value=u'1')
        productcarac2 = self.create_product_caracteristic(product, ftype='choices', name='choices_carac', value=u'choice1')
        product = Product.objects.get(slug=product.slug)
        response = self.client.get(reverse('product-list', kwargs={'slug':category.slug}), {'boolean_carac':'1;b', 'choice_carac':'choice1;c'})
        self.assertEqual(response.context['active_filters'], ['boolean_carac', 'choice_carac'])
        self.assertEqual(response.context['active_values'], ['1;b', 'choice1;c'])
        return
        


        
        