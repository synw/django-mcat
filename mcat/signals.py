# -*- coding: utf-8 -*-

from django.db.models.signals import pre_save, post_save
from mcat.models import CategoryCaracteristic, ProductCaracteristic, Product


def update_product_caracteristics(product, category):
    #~ autocreate product caracteristics on product creation
    carac_types = CategoryCaracteristic.objects.filter(category=category)
    for carac in carac_types:
        c = ProductCaracteristic(product=product, name=carac.slug, type=carac.type, type_name=carac.name)
        c.save()
    return
        
#~ -------------------------- signals -----------------------------
def create_caracteristics(sender, instance, created, **kwargs):
    if created is True:
        update_product_caracteristics(instance, instance.category)
    return

def check_caracteristics(sender, instance, **kwargs):
    old_obj = Product.objects.get(pk=instance.pk)
    old_category = old_obj.category
    category_has_changed = False
    # if category has changed reinitialize product caracteristics
    if old_category != instance.category:
        category_has_changed = True
        #~ reinitialize product caracteristics
        old_obj_caracs = ProductCaracteristic.objects.filter(product=old_obj)
        for carac in old_obj_caracs:
            carac.delete()
        #~ erase product stored caracteristics 
        instance.carac1 = ''
        instance.carac2 = ''
        instance.carac3 = ''
        instance.carac4 = ''
        instance.carac5 = ''
        instance.int_carac1 = None
        instance.int_carac2 = None
        instance.int_carac3 = None
        instance.int_carac1_name = ''
        instance.int_carac2_name = ''
        instance.int_carac3_name = ''
    if category_has_changed is True:
        update_product_caracteristics(instance, instance.category)
    return
    
post_save.connect(create_caracteristics, Product)
pre_save.connect(check_caracteristics, Product)

