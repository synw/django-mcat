# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from django.test import TestCase
from django.conf import settings
from autofixture import AutoFixture
from mcat.models import Category, Product, CategoryCaracteristic, ProductCaracteristic


#@override_settings()
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
    
    """
    @override_settings(DISABLE_BREADCRUMBS=True)
    def test__CategoryViewSettings(self):
        print 'F= '+str(settings.DISABLE_BREADCRUMBS)
        self.create_category(slug='cat1')
        response = self.client.get(reverse('category-list', kwargs={'slug':'cat1'}))
        self.assertTrue(response.context['disable_breadcrumbs'])
        return
    """
    
    def test_ProductsInCategoryView(self):
        self.create_category(slug='cat2')
        category = Category.objects.filter(slug='cat2').prefetch_related('generic_caracteristics')[0]
        last_level=category.level+1
        categories = category.get_descendants().filter(level__lte=last_level)
        self.create_products(category=category)
        products = Product.objects.filter(category=category)
        response = self.client.get(reverse('product-list', kwargs={'slug':category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['products']), list(products))
        self.assertEqual(response.context['category'], category)
        self.assertEqual(list(response.context['categories']), list(categories))
        self.assertEqual(response.context['num_categories'], len(categories))
        self.assertEqual(response.context['num_products'], len(products))
        self.assertTrue(response.context['use_filters'])  
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
        active_filters = {'boolean_carac':'1;b', 'choice_carac':'choice1;c'}
        response = self.client.get(reverse('product-list', kwargs={'slug':category.slug}), active_filters)
        self.assertEqual(response.context['active_filters'], active_filters)
        self.assertEqual(category.template_name, 'default')
        self.assertTemplateUsed(response, 'mcat/products/index.html')
        self.assertFalse('disable_breadcrumbs' in response.context)
        #productcarac3 = self.create_product_caracteristic(product, ftype='int', name='int_carac', value=u'-10')
        product = Product.objects.get(slug=product.slug)
        product.int_carac1 = 8
        product.int_carac1_name = 'int_filter'
        active_filters = {'int_filter':'-10;i'}
        response = self.client.get(reverse('product-list', kwargs={'slug':category.slug}), active_filters)
        self.assertEqual(response.context['active_filters'], active_filters)
        product.int_carac1 = 50
        active_filters = {'int_filter':'+20;i'}
        response = self.client.get(reverse('product-list', kwargs={'slug':category.slug}), active_filters)
        self.assertEqual(response.context['active_filters'], active_filters)
        product.int_carac1 = 5
        active_filters = {'int_filter':'10_20;i'}
        response = self.client.get(reverse('product-list', kwargs={'slug':category.slug}), active_filters)
        self.assertEqual(response.context['active_filters'], active_filters)
        return
    
    """
    @override_settings(DISABLE_BREADCRUMBS=True, USE_FILTERS = False)   
    def test_ProductsInCategoryViewSettings(self):
        self.create_category(slug='cat3')
        response = self.client.get(reverse('product-list', kwargs={'slug':'cat3'}))
        self.assertIsNone(response.context['filters_position'])
        self.assertTemplateUsed(response, 'mcat/products/index._filters_top.html')
        self.assertTrue('disable_breadcrumbs' in response.context)
        return
    """
    
    def test_ProductView(self):
        self.create_category(slug='cat4')
        category = Category.objects.filter(slug='cat4').prefetch_related('generic_caracteristics')[0]
        last_level=category.level+1
        categories = category.get_descendants().filter(level__lte=last_level)
        choices = 'choice1 > Choice 1\nchoice2 > Choice 2'
        self.create_category_caracteristic(category=category, slug='catcarac2', name='carac_name', ftype='choices', choices=choices)
        self.create_category_caracteristic(category=category, slug='catcarac3', name='carac_name', ftype='boolean')
        product = self.create_product(category=category)
        self.create_product_caracteristic(product, ftype='choices', name='catcarac2', value=u'choice1')
        self.create_product_caracteristic(product, ftype='boolean', name='catcarac3', value=u'1')
        response = self.client.get(reverse('product-detail', kwargs={'slug':product.slug, 'category_slug':category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mcat/products/detail.html')
        self.assertEqual(response.context['product'], product)
        self.assertEqual(response.context['category'], category)
        self.assertEqual(list(response.context['categories']), list(categories))
        self.assertEqual(response.context['num_categories'], len(categories))
        self.assertEqual(list(response.context['ancestors']), list(category.get_ancestors()))
        caracs_qs = product.caracteristics.all()
        caracs = {}
        for carac in caracs_qs:
            caracs[carac.type_name] = [carac.type, carac.value_name]
        self.assertEqual(response.context['caracteristics'], caracs)
        return
    
    def test_SearchView(self):
        fixture = AutoFixture(Product, field_values={'name':'prod1', 'upc':'AAA'}, generate_fk=True)
        fixture.create(1)
        fixture = AutoFixture(Product, field_values={'name':'prod2', 'upc':'AAA BBB'}, generate_fk=True)
        fixture.create(1)
        fixture = AutoFixture(Product, field_values={'name':'prod3', 'upc':'AAA BBB CCC'}, generate_fk=True)
        fixture.create(1)
        product1 = Product.objects.get(upc='AAA')
        product2 = Product.objects.get(upc='AAA BBB')
        product3 = Product.objects.get(upc='AAA BBB CCC')
        response = self.client.get(reverse('product-search'),{'q':'BBB'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mcat/search.html')
        self.assertEqual(list(response.context['products']),[product2, product3])
        response = self.client.get(reverse('product-search'),{'q':'prod'})
        self.assertEqual(list(response.context['products']),[product1, product2,product3])
        return
        






        