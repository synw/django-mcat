# -*- coding: utf-8 -*-

from django.test import TestCase
from autofixture import AutoFixture
from mcat.utils import intspace, is_name_in_field, decode_ftype, encode_ftype
from mcat.models import ProductCaracteristic


class McatUtilsTest(TestCase):
    
    def test_intspace(self):
        num = '10000'
        self.assertEqual(intspace(num), '10 000')
        num = '100'
        self.assertNotEqual(intspace(num), '1 00')
        return
    
    def create_product_caracteristic(self):
        fixture = AutoFixture(ProductCaracteristic, field_values={'name':'carac1_n','value':'0'}, generate_fk=True)
        fixture.create(1)
    
    def test_is_name_in_field(self):
        self.create_product_caracteristic()
        pcarac = ProductCaracteristic.objects.get(pk=1)
        field_val = 'carac1_n:1;boolean'
        ftype = 'boolean'
        name = pcarac.name
        self.assertTrue(is_name_in_field(name, field_val))
        return
    
    def test_decode_ftype(self):
        raw_ftype = 'c'
        self.assertTrue(decode_ftype(raw_ftype), 'choices')
        raw_ftype = 'i'
        self.assertTrue(decode_ftype(raw_ftype), 'int')
        raw_ftype = 'b'
        self.assertTrue(decode_ftype(raw_ftype), 'boolean')
        raw_ftype = 'z'
        self.assertFalse(decode_ftype(raw_ftype), 'boolean')
        return
    
    def encode_ftype(self):
        raw_ftype = 'choices'
        self.assertTrue(encode_ftype(raw_ftype), 'c')
        raw_ftype = 'int'
        self.assertTrue(encode_ftype(raw_ftype), 'i')
        raw_ftype = 'boolean'
        self.assertTrue(encode_ftype(raw_ftype), 'b')
        raw_ftype = 'zzz'
        self.assertFalse(encode_ftype(raw_ftype), 'b')
        return



