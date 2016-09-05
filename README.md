# Django Mcat

Product catalog for Django. 

This app wants to be:

- Fast
- Fully responsive and optimized for phone devices
- Maintainable and extensible by the use of straigthforward Django and understandable code

It is scalable: can be used whith or without prices management, product filters, automatic breadcrumbs, brands. 
All this is configurable in the settings. Each option that is disabled makes the app faster,
so be sure to enable only what you need.

Why this app? It was made to handle the job with a minimum of complexity, keeping the code simple. It was designed
to be fast. Working with stuff like big ecommerce frameworks is nice but can sometimes become a pain when you want 
to extend them or get into the code, due to its level of complexity.

### Install

Get the dependencies:

  ```bash
pip install django-watson django-jsonfield sorl-thumbnail
  ```

Add to installed apps:

  ```python
"sorl.thumbnail",
"watson",
"mcat",
  ```

Set the urls

  ```python
url('^catalog/', include('mcat.urls')),
  ```

### Settings

Default values are:

  ```python
MCAT_USE_PRICES = True

MCAT_CURRENCY = '$' # currency representation

MCAT_PRICES_AS_INTEGER = False # otherwise prices are float

MCAT_USE_FILTERS = True # product filters

MCAT_USE_PRICE_FILTER = True # filter on prices

MCAT_CODE_MODE = False # edit product descriptions in an html editor rather than in the default wysiwyg one

MCAT_USE_BRAND = False

MCAT_PAGINATE_BY = 10

MCAT_DISABLE_BREADCRUMBS = False

MCAT_CATEGORY_TEMPLATE_NAMES = (
                    ('default',_(u'Filters on side')),
                    ('filters_on_top',_(u'Filters on top')),
                    ('fullwidht_filters_on_top',_(u'Fullwidth filters on top')),
                    )

MCAT_PRODUCT_TEMPLATE_NAMES = (
                    ('default',_(u'Default')),
                    ('detail_fullwidth_slideshow',_(u'Fullwidth slideshow')),
                    )


MCAT_CATEGORY_TEMPLATE_NAMES = (
                    ('default',_(u'Filters on side')),
                    ('filters_on_top',_(u'Filters on top')),
                    ('fullwidht_filters_on_top',_(u'Fullwidth filters on top')),
                    )

  ```

