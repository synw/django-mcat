# -*- coding: utf-8 -*-


from django import template
from django.template import Library, Node, resolve_variable
from mcat.conf import CURRENCY, PRICES_AS_INTEGER
from mcat.utils import intspace

register = template.Library()

@register.filter(is_safe=True)
def format_price(product):
    price = product.get_price()
    if PRICES_AS_INTEGER:
        price = intspace(int(round(price)))
    price = str(price)
    return price+'&nbsp;'+CURRENCY


class AddGetParameter(Node):
    def __init__(self, values):
        self.values = values
        
    def render(self, context):
        req = resolve_variable('request', context)
        params = req.GET.copy()
        for key, value in self.values.items():
            params[resolve_variable(key, context)] = value.resolve(context)
        if 'page' in params.keys():
            del params['page']
        return '?%s' %  params.urlencode({' ' : ''})
    

class RemoveGetParameter(Node):
    def __init__(self, values):
        self.values = values
        
    def render(self, context):
        req = resolve_variable('request', context)
        params = req.GET.copy()
        for key in self.values.keys():
            del params[resolve_variable(key, context)]
        if 'page' in params.keys():
            del params['page']
        return '?%s' %  params.urlencode({' ' : ''})
    

@register.tag
def append_to_get(parser, token):
    pairs = token.split_contents()[1:]
    values = {}
    s = pairs[0].split('=', 1)
    name = s[1]
    s = pairs[1].split('=', 1)
    value = s[1]
    values[name] = parser.compile_filter(unicode.strip(value))
    return AddGetParameter(values)

@register.tag
def remove_from_get(parser, token):
    pairs = token.split_contents()[1:]
    values = {}
    s = pairs[0].split('=', 1)
    name = s[1]
    s = pairs[1].split('=', 1)
    value = s[1]
    values[name] = parser.compile_filter(unicode.strip(value))
    return RemoveGetParameter(values)

@register.simple_tag
def pagenum_replace(request, value):
    dict_ = request.GET.copy()
    dict_['page'] = value
    print str(dict_)
    return dict_.urlencode()




