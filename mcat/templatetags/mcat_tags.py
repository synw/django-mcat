# -*- coding: utf-8 -*-


from django import template
from mcat.conf import CURRENCY

register = template.Library()

@register.filter
def format_price(product):
    return str(product.get_price())+' '+CURRENCY