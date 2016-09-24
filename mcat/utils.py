# -*- coding: utf-8 -*-

import re
import qrcode
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.encoding import force_unicode
from mcat.conf import USE_PRICES, PRICES_AS_INTEGER


def generate_qr_image(data, protocol, qrversion=1):
        qr = qrcode.QRCode(
            version=qrversion,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=4,
        )
        separator = ':'
        if protocol == 'http':
            separator = '://'
        qr.add_data(protocol+separator+str(data))
        qr.make()
        thumb = qr.make_image()
        return thumb
    
def generate_qr_file(filename, data, protocol='http',qrversion=1):
        thumb = generate_qr_image(data, protocol, qrversion)
        #~ save image to field
        thumb_io = StringIO.StringIO()
        thumb.save(thumb_io)
        filename = filename+'.png'
        thumb_file = InMemoryUploadedFile(thumb_io, None, filename, 'image/png',thumb_io.len, None)
        return thumb_file

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

def is_name_in_field(val, field_val):
    v = field_val.split(';')[0]
    v = v.split(':')[0]
    if val == v:
        return True
    return False

def decode_ftype(raw_ftype):
    ftype = ''
    if raw_ftype == 'c':
        ftype = 'choices'
    if raw_ftype == 'i':
        ftype = 'int'
    if raw_ftype == 'b':
        ftype = 'boolean'
    return ftype

def encode_ftype(raw_ftype):
    ftype = ''
    if raw_ftype == 'choices':
        ftype = 'c'
    if raw_ftype == 'int':
        ftype = 'i'
    if raw_ftype == 'boolean':
        ftype = 'b'
    return ftype

def get_min_max_prices(products):
    min_ = 0
    max_ = 0
    i = 0
    for product in products:
        if i==0 or product.price < min_:
            min_ = product.price
        if i==0 or product.price > max_:
            max_ = product.price  
        i+=1 
    return (min_, max_)

def get_price(price):
    if USE_PRICES is True and price:
        if PRICES_AS_INTEGER is True:
            price = int(round(price))
    return price