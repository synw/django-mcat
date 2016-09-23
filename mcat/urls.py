# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from mcat.views import IndexView, ProductView, CategoryHomeView, CategoryView, ProductsInCategoryView, SearchView
from mcat.conf import USE_ORDER

if USE_ORDER is True:
    urlpatterns = [ url('^order/', include('mcat_order.urls')) ]
else:
    urlpatterns = []

urlpatterns.append(url(r'^product/(?P<category_slug>[-_\w]+)/(?P<slug>[-_\w]+)/$', ProductView.as_view(), name="product-detail"))
urlpatterns.append(url(r'^products/(?P<slug>[-_\w]+)/$', ProductsInCategoryView.as_view(), name="product-list"))
urlpatterns.append(url(r'^search/$', SearchView.as_view(), name="product-search"))
urlpatterns.append(url(r'^categories/$', CategoryHomeView.as_view(), name="category-home"))
urlpatterns.append(url(r'^(?P<slug>[-_\w]+)/$', CategoryView.as_view(), name="category-list"))
urlpatterns.append(url(r'^', IndexView.as_view(), name="category-home"))

