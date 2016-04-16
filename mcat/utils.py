# -*- coding: utf-8 -*-


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

