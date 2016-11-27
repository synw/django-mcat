# -*- coding: utf-8 -*-


from django import template
from django.template import Node, Variable
from mcat.conf import CURRENCY, PRICES_AS_INTEGER
from mcat.utils import intspace, get_price

register = template.Library()

@register.filter(is_safe=True)
def format_price(price):
    price = get_price(price)
    price = str(intspace(price))
    return price+'&nbsp;'+CURRENCY

@register.simple_tag
def format_from_price(price, currency=True):
    if price is None:
        price = ''
        currency = False
    if PRICES_AS_INTEGER is True and price is not None:
        try:
            price = intspace(int(round(price)))
        except:
            pass
    price = str(price)
    if currency is True:
        return price+' '+CURRENCY
    else:
        return price


class AddGetParameter(Node):
    def __init__(self, values):
        self.values = values
        
    def render(self, context):
        req = Variable('request', context)
        params = req.GET.copy()
        for key, value in self.values.items():
            params[Variable(key, context)] = value.resolve(context)
        if 'page' in params.keys():
            del params['page']
        return '?%s' %  params.urlencode({' ' : ''})
    

class RemoveGetParameter(Node):
    def __init__(self, values):
        self.values = values
        
    def render(self, context):
        req = Variable('request', context)
        params = req.GET.copy()
        for key in self.values.keys():
            del params[Variable(key, context)]
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
    return dict_.urlencode()

@register.assignment_tag
def is_active_filter(filterset, name, value):
    if bool(filterset) is True:
        for key, val in filterset.items():
            if val == value and key==name:
                return True
    return False

