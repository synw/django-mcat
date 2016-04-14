# -*- coding: utf-8 -*-

from django.db.models import Q, Prefetch
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.utils.html import strip_tags
from mcat.models import Category, Product, ProductCaracteristic
from mcat.conf import DISABLE_BREADCRUMBS, FILTERS_POSITION


class CategoryHomeView(TemplateView):
    template_name = 'mcat/categories/index.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryHomeView, self).get_context_data(**kwargs)
        categories = Category.objects.filter(level__lte=0, status=0)
        context['categories'] = categories
        context['num_categories'] = len(categories)
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
        return context


class ProductsInCategoryView(ListView):
    template_name = 'mcat/products/index.html'
    paginate_by = 10 
    context_object_name = 'products'
    
    def get_queryset(self):
        self.category=get_object_or_404(Category.objects.prefetch_related('generic_caracteristics'), slug=self.kwargs['slug'], status=0)
        self.caracteristics = self.category.generic_caracteristics.all()
        
        products=Product.objects.filter(category=self.category, status=0).prefetch_related('caracteristics')
        #~ get the requested filters
        self.filters = None
        if self.request.GET:
            filters = {}
            for param, value in self.request.GET.items():
                filters[param] = value.replace('+','')
            #~ filter on products
            for name, value in filters.items():
                val = name+':'+value
                products = products.filter(Q(carac1=val)|Q(carac2=val)|Q(carac3=val)|Q(carac4=val)|Q(carac5=val)|Q(carac6=val)|Q(carac7=val)|Q(carac8=val))
            self.filters = filters
        return products

    def get_context_data(self, **kwargs):
        context = super(ProductsInCategoryView, self).get_context_data(**kwargs)
        category= self.category
        last_level=category.level+1
        categories = category.get_descendants().filter(level__lte=last_level)
        if DISABLE_BREADCRUMBS:
            context['disable_breadcrumbs'] = True
        else:
            context['ancestors'] = category.get_ancestors()
        context['category'] = category
        context['categories'] = categories
        context['caracteristics'] = self.caracteristics
        context['num_categories'] = len(categories)
        context['filters_position'] = FILTERS_POSITION
        if self.filters:
            context['active_filters'] = self.filters.keys()
            context['active_values'] = self.filters.values()
        return context
    
    
class ProductView(TemplateView):
    template_name = 'mcat/products/detail.html'
   
    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        #~ get the data
        category=get_object_or_404(Category, slug=self.kwargs['category_slug'], status=0)
        product=get_object_or_404(Product, slug=self.kwargs['slug'], status=0)
        last_level=category.level+1
        categories = category.get_descendants().filter(level__lte=last_level).order_by('name')
        if DISABLE_BREADCRUMBS:
            context['disable_breadcrumbs'] = True
        else:
            context['ancestors'] = category.get_ancestors()
        #~ fill context
        context['slideshow'] = object
        context['category'] = category
        context['categories'] = categories
        context['product'] = product
        context['num_categories'] = len(categories)
        return context


class SearchView(ListView):
    template_name = 'mcat/search.html'
    paginate_by = 10 
    context_object_name = 'products'
    
    def get_queryset(self):
        products = Product.objects.filter(status=0).prefetch_related('images', 'category')
        if "q" in self.request.GET.keys():
            q = strip_tags(self.request.GET['q'])
            products = products.filter(Q(name__icontains=q)|Q(upc__icontains=q))
        #self.category=get_object_or_404(Category, slug=self.kwargs['slug'], status=0)
        #products=Product.objects.filter(category=self.category, status=0).prefetch_related('images')
        return products
    
    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)

        return context


    

