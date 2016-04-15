# -*- coding: utf-8 -*-

from django.db.models.signals import post_save
from mcat.models import CategoryCaracteristic, ProductCaracteristic, Product

def create_caracteristics(sender, instance, created, **kwargs):
    if created:
        #~ autocreate product caracteristics on product creation
        carac_types = CategoryCaracteristic.objects.filter(category=instance.category)
        for carac in carac_types:
            c = ProductCaracteristic(product=instance, name=carac.slug)
            c.save()
    return
    
post_save.connect(create_caracteristics, Product)