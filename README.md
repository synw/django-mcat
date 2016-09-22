# Django Mcat

Product catalog for Django. 

This app wants to be:

- Fast
- Fully responsive and optimized for phone devices
- Maintainable and extensible by the use of straigthforward idiomatic Django code

It is scalable: can be used whith or without prices management, product filters, automatic breadcrumbs, brands. 
All this is configurable in the settings. Each option that is disabled makes the app faster,
so be sure to enable only what you need.

Why this app? It was made to handle the job with a minimum of complexity, keeping the code simple. It was designed
to be fast. Working with stuff like big ecommerce frameworks is nice but can sometimes become a pain when you want 
to extend them or get into the code, due to its level of complexity.

### Install

Get the dependencies:

  ```bash
pip install django-watson django-jsonfield easy-thumbnails django-ckeditor
  ```

Add to installed apps:

  ```python
"easy_thumbnails",
"watson",
"mcat",
  ```

Set the urls

  ```python
url(r'^ckeditor/',include('ckeditor_uploader.urls')),
url('^catalog/', include('mcat.urls')),
  ```
  
Ckeditor and easy thumbnails configuration in settings.py:

  ```python
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_JQUERY_URL = '/static/js/jquery-2.1.4.min.js'
CKEDITOR_CONFIGS = {
    'mcat': {
        'toolbar':  [
                    ["Format", "Styles", "Bold", "Italic", "Underline", '-', 'RemoveFormat'],
                    ['NumberedList', 'BulletedList', "Indent", "Outdent", 'JustifyLeft', 'JustifyCenter','JustifyRight', 'JustifyBlock'],
                    ["Image", "Table", "Link", "Unlink", "Anchor", "SectionLink", "Subscript", "Superscript"], ['Undo', 'Redo'],
                    ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord'],["Source", "Maximize"],
                    ],
        "removePlugins": "stylesheetparser",
        'width': '1150px',
        'height': '400px',
    },
}

THUMBNAIL_ALIASES = {
    '': {
        'square': {'size': (200, 200), 'crop': False},
    },
}
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
  ```

