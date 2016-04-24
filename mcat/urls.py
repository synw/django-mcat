# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import patterns, url, include
from mcat.views import ProductView, CategoryHomeView, CategoryView, ProductsInCategoryView, SearchView
from mcat.conf import USE_ORDER

if USE_ORDER:
    urlpatterns = patterns('', 
    url('^order/', include('mcat_order.urls')),
    url(r'^product/(?P<category_slug>[-_\w]+)/(?P<slug>[-_\w]+)/$', ProductView.as_view(), name="product-detail"),
    url(r'^products/(?P<slug>[-_\w]+)/$', ProductsInCategoryView.as_view(), name="product-list"),
    url(r'^search/$', SearchView.as_view(), name="product-search"),
    url(r'^(?P<slug>[-_\w]+)/$', CategoryView.as_view(), name="category-list"),
    url(r'^', CategoryHomeView.as_view(), name="category-home"),
    )
else:
    urlpatterns = patterns('', 
    url(r'^product/(?P<category_slug>[-_\w]+)/(?P<slug>[-_\w]+)/$', ProductView.as_view(), name="product-detail"),
    url(r'^products/(?P<slug>[-_\w]+)/$', ProductsInCategoryView.as_view(), name="product-list"),
    url(r'^search/$', SearchView.as_view(), name="product-search"),
    url(r'^(?P<slug>[-_\w]+)/$', CategoryView.as_view(), name="category-list"),
    url(r'^', CategoryHomeView.as_view(), name="category-home"),
    )

