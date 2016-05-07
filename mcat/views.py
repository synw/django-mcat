# -*- coding: utf-8 -*-

from django.db.models import Q, Max, Min
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, Http404, render_to_response
from django.utils.html import strip_tags
from django.conf import settings
from watson import search as watson
from mcat.models import Category, Product
from mcat.conf import PAGINATE_BY, DISABLE_BREADCRUMBS, USE_FILTERS, USE_PRICES, USE_ORDER, USE_BRAND, USE_PRICE_FILTER, PRICES_AS_INTEGER, CURRENCY
from mcat.utils import decode_ftype, get_min_max_prices


class CategoryHomeView(TemplateView):
    template_name = 'mcat/categories/index.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryHomeView, self).get_context_data(**kwargs)
        categories = Category.objects.filter(level__lte=0, status=0)
        context['categories'] = categories
        context['num_categories'] = len(categories)
        if USE_ORDER:
            context['use_order'] = True
        return context
    
    
class CategoryView(TemplateView):
    template_name = 'mcat/categories/browse.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        current_category=get_object_or_404(Category, slug=self.kwargs['slug'])
        last_level=current_category.level+1
        categories = current_category.get_descendants().filter(level__lte=last_level, status=0)
        if DISABLE_BREADCRUMBS:
            context['disable_breadcrumbs'] = True
        else:
            context['ancestors'] = current_category.get_ancestors()
        context['current_category'] = current_category
        context['categories'] = categories
        context['num_categories'] = len(categories)
        if USE_ORDER:
            context['use_order'] = True
        return context


class ProductsInCategoryView(ListView):
    paginate_by = PAGINATE_BY
    context_object_name = 'products'
    
    def get_queryset(self):
        self.category=get_object_or_404(Category.objects.prefetch_related('generic_caracteristics'), slug=self.kwargs['slug'], status=0)
        products=Product.objects.filter(category=self.category, status=0).prefetch_related('caracteristics')
        self.caracteristics = self.category.generic_caracteristics.all()
        #~ get the requested filters
        self.filters = None
        if self.request.GET and USE_FILTERS:
            filters = {}
            for param, value in self.request.GET.items():
                if not param == 'page':
                    filters[param] = value
            #~ filter on products            
            for name, value in filters.items():
                raw_ftype = value.split(';')[1]
                ftype = decode_ftype(raw_ftype)
                if ftype in ['choices', 'boolean']:
                    val = name+':'+value.replace(raw_ftype, ftype)
                    products = products.filter(Q(carac1=val)|Q(carac2=val)|Q(carac3=val)|Q(carac4=val)|Q(carac5=val))
                elif ftype == 'int':
                    if '_' in value:
                        frange = value.split(';')[0].split('_')
                        start_range = frange[0]
                        end_range = frange[1]
                        products = products.filter(Q(int_carac1_name=name, int_carac1__gte=start_range, int_carac1__lte=end_range)|Q(int_carac2_name=name, int_carac2__gte=start_range, int_carac2__lte=end_range)|Q(int_carac3_name=name, int_carac3__gte=start_range, int_carac3__lte=end_range))
                    else:
                        if value.startswith('-'):
                            val = value[1:].split(';')[0]
                            products = products.filter(Q(int_carac1_name=name, int_carac1__lt=val))
                        elif value.startswith('+'):
                            val = value[1:].split(';')[0]
                            products = products.filter(Q(int_carac1_name=name, int_carac1__gt=val))                     
            self.filters = filters
        self.num_products = len(products)
        if USE_PRICES and USE_FILTERS and USE_PRICE_FILTER:
            self.min_price, self.max_price = get_min_max_prices(products)
            if PRICES_AS_INTEGER:
                try:
                    self.min_price = int(round(self.min_price))
                    self.max_price = int(round(self.max_price))
                except:
                    pass
        return products

    def get_context_data(self, **kwargs):
        context = super(ProductsInCategoryView, self).get_context_data(**kwargs)
        category= self.category
        last_level=category.level+1
        categories = category.get_descendants().filter(level__lte=last_level)
        if DISABLE_BREADCRUMBS is True:
            context['disable_breadcrumbs'] = True
        else:
            context['ancestors'] = category.get_ancestors()
        context['category'] = category
        context['categories'] = categories
        context['caracteristics'] = self.caracteristics
        context['num_categories'] = len(categories)
        context['num_products'] = self.num_products
        if self.filters is not None:
            context['active_filters'] = self.filters
        context['use_filters'] = USE_FILTERS
        if USE_PRICES is False:
            context['no_prices'] = True
            context['currency'] = CURRENCY
        else:
            if USE_PRICE_FILTER is True:
                context['use_price_filter'] = True
                context['min_price'] = self.min_price
                context['max_price'] = self.max_price
        if USE_ORDER:
            context['use_order'] = True
        return context
    
    def get_template_names(self):
        template_name = self.category.template_name
        if template_name == 'default':
            return 'mcat/products/index.html'
        else:
            return 'mcat/products/alt/'+template_name+'.html'


class ProductView(TemplateView):
   
    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        #~ get the data
        category=get_object_or_404(Category, slug=self.kwargs['category_slug'], status=0)
        if USE_BRAND:
            product=get_object_or_404(Product.objects.prefetch_related('images','caracteristics','brand'), slug=self.kwargs['slug'], status=0)
        else:
            product=get_object_or_404(Product.objects.prefetch_related('images','caracteristics'), slug=self.kwargs['slug'], status=0)
        last_level=category.level+1
        categories = category.get_descendants().filter(level__lte=last_level).order_by('name')
        self.template_name = product.template_name
        #~ get product caracteristics
        caracs = {}
        for carac in product.caracteristics.all():
            caracs[carac.type_name] = [carac.type, carac.value_name]
        if DISABLE_BREADCRUMBS:
            context['disable_breadcrumbs'] = True
        else:
            context['ancestors'] = category.get_ancestors()
        #~ fill context
        context['category'] = category
        context['categories'] = categories
        context['product'] = product
        context['num_categories'] = len(categories)
        context['caracteristics'] = caracs
        if USE_PRICES is False:
            context['no_prices'] = True
        if USE_ORDER:
            context['use_order'] = True
        if USE_BRAND:
            context['use_brand'] = True
        if product.extra:
            context['url_assistance'] = product.extra['url_assistance']
            context['url_notice'] = product.extra['url_notice']
        return context
    
    def get_template_names(self):
        template_name = self.template_name
        if template_name == 'default':
            return 'mcat/products/detail.html'
        else:
            return 'mcat/products/alt/'+template_name+'.html'


class SearchView(ListView):
    template_name = 'mcat/search.html'
    paginate_by = PAGINATE_BY
    context_object_name = 'products'
    
    def get_queryset(self):
        if "q" in self.request.GET.keys():
            products = Product.objects.filter(status=0).prefetch_related('images', 'category')
            q = self.q = strip_tags(self.request.GET['q'])
            search_results = watson.filter(products, q)
            
            for product in search_results:
                print product.name+' / '+str(product.category)
            
        return search_results
        """
        products = Product.objects.filter(status=0).prefetch_related('images', 'category')
        if "q" in self.request.GET.keys():
            q = strip_tags(self.request.GET['q'])
            q_words = q.split(' ')
            for word in q_words: 
                products = products.filter(Q(name__icontains=word)|Q(upc__icontains=word))
        self.q = q
        return products
        """
    
    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        if USE_ORDER:
            context['use_order'] = True
        context['search'] = True
        context['user_query'] = self.q
        return context







