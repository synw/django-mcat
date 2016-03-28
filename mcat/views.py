# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from mcat.models import Category, Product, Brand
from mcat.conf import DISABLE_BREADCRUMBS

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
        self.category=get_object_or_404(Category, slug=self.kwargs['slug'], status=0)
        products=Product.objects.filter(category=self.category, status=0).prefetch_related('images')
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
        context['num_categories'] = len(categories)
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


