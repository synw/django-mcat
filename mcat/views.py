# -*- coding: utf-8 -*-

from django.db.models import Q
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, Http404, render_to_response
from django.utils.html import strip_tags
from django.conf import settings
from mcat.models import Category, Product
from mcat.conf import DISABLE_BREADCRUMBS, USE_FILTERS, USE_PRICES
from mcat.utils import decode_ftype


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
    paginate_by = 10
    context_object_name = 'products'
    
    def get_queryset(self):
        self.category=get_object_or_404(Category.objects.prefetch_related('generic_caracteristics'), slug=self.kwargs['slug'], status=0)
        products=Product.objects.filter(category=self.category, status=0).prefetch_related('caracteristics')
        self.caracteristics = self.category.generic_caracteristics.all()
        #~ get the requested filters
        self.filters = None
        if USE_FILTERS is False:
            self.filters_position = None
        else:
            self.filters_position = self.category.filters_position
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
        context['use_filters'] = USE_FILTERS
        if self.filters is not None:
            context['active_filters'] = self.filters.keys()
            context['active_values'] = self.filters.values()
        context['filters_position'] = self.filters_position
        if USE_PRICES is False:
            context['no_prices'] = True  
        return context
    
    def get_template_names(self):
        if self.filters_position == 'side':
            return 'mcat/products/index.html'
        else:
            return 'mcat/products/index_filters_top.html'


class ProductView(TemplateView):
    template_name = 'mcat/products/detail.html'
   
    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        #~ get the data
        category=get_object_or_404(Category, slug=self.kwargs['category_slug'], status=0)
        product=get_object_or_404(Product.objects.prefetch_related('images','caracteristics'), slug=self.kwargs['slug'], status=0)
        last_level=category.level+1
        categories = category.get_descendants().filter(level__lte=last_level).order_by('name')
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

"""   
def add_to_cart(request, slug):
    if request.is_ajax():
        cart = Cart(request.session)
        product = get_object_or_404(Product, slug=slug)
        cart.add(product, price=product.price)
        return render_to_response('mcat/cart/add.html',
                                   {'product' : product},
                                   content_type="application/xhtml+xml"
                                   )
    else:
        if settings.DEBUG:
            print "Not ajax request"
        raise Http404

"""





