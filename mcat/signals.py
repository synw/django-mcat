from __future__ import print_function
from django.db.models.signals import pre_save, post_save, pre_delete
from mcat.models import CategoryCaracteristic, ProductCaracteristic, Product


DEBUG_MODE = False

def cleanup_product_caracteristics(product):
    if DEBUG_MODE is True:
        print('Cleaning up product caracteristics index')
    old_obj_caracs = ProductCaracteristic.objects.filter(product=product)
    for carac in old_obj_caracs:
        carac.delete()
    #~ erase product stored caracteristics 
    product.carac1 = ''
    product.carac2 = ''
    product.carac3 = ''
    product.carac4 = ''
    product.carac5 = ''
    product.int_carac1 = None
    product.int_carac2 = None
    product.int_carac3 = None
    product.int_carac1_name = ''
    product.int_carac2_name = ''
    product.int_carac3_name = ''
    return product

def remove_product_caracteristic(product, carac_name):
    if DEBUG_MODE is True:
        print('Trying to remove caracteristic '+carac_name+' from product')
    if carac_name in product.carac1:
        product.carac1 = ''
    elif carac_name in product.carac2:
        product.carac2 = ''
    elif carac_name in product.carac3:
        product.carac3 = ''
    elif carac_name in product.carac4:
        product.carac4 = ''
    elif carac_name in product.carac5:
        product.carac5 = ''
    elif carac_name in product.int_carac1_name:
        product.int_carac1 = None
        product.int_carac1_name = ''
    elif carac_name in product.int_carac2_name:
        product.int_carac2 = None
        product.int_carac2_name = ''
    elif carac_name in product.int_carac3_name:
        product.int_carac3 = None
        product.int_carac3_name = ''
    return product
    

def create_product_caracteristics(product, category):
    #~ autocreate product caracteristics on product creation
    carac_types = CategoryCaracteristic.objects.filter(category=category)
    for carac in carac_types:
        c = ProductCaracteristic(product=product, name=carac.slug, type=carac.type, type_name=carac.name)
        c.save()
        if DEBUG_MODE is True:
            print('Product caracterist '+str(c)+' saved')
    return
        
#~ -------------------------- signals -----------------------------
def create_caracteristics(sender, instance, created, **kwargs):
    if DEBUG_MODE is True:
        print('SIGNAL: create_caracteristics (post_save '+str(instance)+' ) -------------------------------')
    if created is True:
        create_product_caracteristics(instance, instance.category)
    if DEBUG_MODE is True:
        print('ENDSIGNAL create_caracteristics')
    return

def check_caracteristics(sender, instance, **kwargs):
    if DEBUG_MODE is True:
        print('SIGNAL : check_caracteristics (pre_save '+str(instance)+' ) ---------------------------------')
    try:
        old_obj = Product.objects.get(pk=instance.pk)
    except:
        return
    old_category = old_obj.category
    # if category has changed reinitialize product caracteristics
    if old_category != instance.category:
        if DEBUG_MODE is True:
            print('Category changed')
        #~ delete old product caracteristics objects
        product_caracs = ProductCaracteristic.objects.filter(product=instance)
        #~ reinitialize product caracteristics index
        if DEBUG_MODE is True:
            print("Old obj : "+str(old_obj))
            print('Old category : '+str(old_category))
            print('New category : '+str(instance.category))
            print('Old caracs : '+str(product_caracs))
        instance = cleanup_product_caracteristics(instance)
        # delete product caracteristics
        for old_carac in product_caracs:
            if DEBUG_MODE is True:
                print('>>>>>>>>> deleting '+str(old_carac))
            old_carac.delete()
        create_product_caracteristics(instance, instance.category)
    if DEBUG_MODE is True:
        print('ENDSIGNAL check_caracteristics')
    return

def delete_category_caracteristic(sender, instance, **kwargs):
    carac = instance
    product_caracs = ProductCaracteristic.objects.filter(name=carac.slug, type=carac.type, type_name=carac.name).select_related('product')
    for product_carac in product_caracs:
        #~ update product
        product = product_carac.product
        remove_product_caracteristic(product, product_carac)
        #~ then delete caracteristic
        product_carac.delete()
    return

def check_product_caracteristic(sender, instance, **kwargs):
    if DEBUG_MODE is True:
        print('SIGNAL: check_product_caracteristic (pre_delete '+str(instance)+' ) -------------------------------')
    product = instance.product
    product = remove_product_caracteristic(product, instance.name)
    product.save()
    if DEBUG_MODE is True:
        print('Product caracteristics :')
        print(product.print_caracteristics())
        print('ENDSIGNAL check_product_caracteristic')
    return
   

# initialize product caracteristics
post_save.connect(create_caracteristics, Product)
# to reinitialize the caracteristics index if the product was moved to another category    
pre_save.connect(check_caracteristics, Product)
# update product caracteristics on category caracteristic deletion
pre_delete.connect(delete_category_caracteristic, CategoryCaracteristic)

pre_delete.connect(check_product_caracteristic, ProductCaracteristic)

