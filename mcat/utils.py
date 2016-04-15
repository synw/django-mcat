# -*- coding: utf-8 -*-


def is_val_in_field(val, field_val):
    val = val.split(':')[0]
    name = field_val.split(':')[0]
    if val == name:
        return True
    return False


