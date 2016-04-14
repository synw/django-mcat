# -*- coding: utf-8 -*-


from django import template
from django.template import Library, Node, resolve_variable
from mcat.conf import CURRENCY

register = template.Library()

@register.filter
def format_price(product):
    return str(product.get_price())+'&nbsp;'+CURRENCY


class AddGetParameter(Node):
    def __init__(self, values):
        self.values = values
        
    def render(self, context):
        req = resolve_variable('request', context)
        params = req.GET.copy()
        for key, value in self.values.items():
            params[resolve_variable(key, context)] = value.resolve(context)
        return '?%s' %  params.urlencode({' ' : ''})
    

class RemoveGetParameter(Node):
    def __init__(self, values):
        self.values = values
        
    def render(self, context):
        req = resolve_variable('request', context)
        params = req.GET.copy()
        for key, value in self.values.items():
            del params[resolve_variable(key, context)]
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



