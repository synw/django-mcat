# -*- coding: utf-8 -*-

import re
from django.utils.encoding import force_unicode


def intspace(value):
    """
    Converts an integer to a string containing spaces every three digits.
    For example, 3000 becomes '3 000' and 45000 becomes '45 000'.
    See django.contrib.humanize app
    """
    orig = force_unicode(value)
    new = re.sub("^(-?\d+)(\d{3})", '\g<1> \g<2>', orig)
    if orig == new:
        return new
    else:
        return intspace(new)


def is_val_in_field(val, field_val):
    val = val.split(':')[0]
    name = field_val.split(':')[0]
    if val == name:
        return True
    return False

def decode_ftype(raw_ftype):
    ftype = 'd'
    if raw_ftype == 'c':
        ftype = 'choices'
    if raw_ftype == 'i':
        ftype = 'int'
    if raw_ftype == 'b':
        ftype = 'boolean'
    return ftype

def encode_ftype(raw_ftype):
    ftype = 'd'
    if raw_ftype == 'choices':
        ftype = 'c'
    if raw_ftype == 'int':
        ftype = 'i'
    if raw_ftype == 'boolean':
        ftype = 'b'
    return ftype

