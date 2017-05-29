from __future__ import print_function
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from mcat.models import Product, ProductImage, ProductCaracteristic, CategoryCaracteristic, Category, Brand
from mcat.forms import BrandForm, CategoryForm, ProductForm, ProductCaracteristicInlineForm


#~ ========================================= Inlines ==================================

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    fields = ['image', 'order']
    extra = 0
    

class ProductCaracteristicInline(admin.TabularInline):
    model = ProductCaracteristic
    form = ProductCaracteristicInlineForm
    readonly_fields = ('name',)
    extra = 0
    
    def get_formset(self, request, obj=None, **kwargs):
        ProductCaracteristicInlineForm.obj = obj
        return super(ProductCaracteristicInline, self).get_formset(request, obj, **kwargs)


class CategoryCaracteristicInline(admin.TabularInline):
    model = CategoryCaracteristic
    fields = ['name', 'slug','type','choices','unit','order']
    prepopulated_fields = {"slug": ("name",)}
    extra = 0

#~ ========================================= Admin classes ==================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    date_hierarchy = 'edited'
    raw_id_fields = ['category','brand']
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name','brand', 'price', 'category','upc','created','status','editor']
    list_filter = ['status', 'created','edited']
    search_fields = ['name','upc','brand__name','category__name','editor__username']
    list_select_related = ['editor','brand','category']
    readonly_fields = ['editor', 'qrcode']
    save_on_top = True
    fieldsets = (
        ("Description du produit", {
            'classes': ('collapse',),
            'fields': ('description',)
        }),
        (None, {
            'fields': (('name', 'slug'), ('category', 'brand'), ('navimage', 'upc'))
        }),
        (None, {
            'fields': (('price', 'available'),)
        }),
        (None, {
            'fields': (('status', 'short_description'), ('template_name'))
        }),
        (_(u'Slideshow options'), {
            'classes': ('collapse',),
            'fields': (('slideshow_type',), ('slideshow_width', 'slideshow_height') )
        }),
        (_(u'Deal'), {
            'classes': ('collapse',),
            'fields': (
                        ('discounted_price', 'discounted_percentage', 'deal_type'), 
                        ('deal_description', 'deal_conditions',),
                        ('deal_start_date', 'deal_end_date'),
                        )
        }),
        (_(u'Extra infos'), {
            'classes': ('collapse',),
            'fields': (('extra', 'qrcode'),)
        }),
    )
    
    def form_valid(self, form):
        """This is what's called when the form is valid."""
        instance = form.save(commit=False)
        #print("Form valid ----------------")
        return super(ProductAdmin, self).form_valid(form)
    
    def form_invalid(self, form):
        """This is what's called when the form is valid."""
        instance = form.save(commit=False)
        #print("Form invalid ----------------")
        return super(ProductAdmin, self).form_invalid(form)
        
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'editor', None) is None:
            obj.editor = request.user
        obj.save()
        return
        
    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = [ProductImageInline]
        return super(ProductAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = [ProductImageInline, ProductCaracteristicInline]
        return super(ProductAdmin, self).change_view(request, object_id, form_url, extra_context)
        
        
@admin.register(Category)    
class CategoryAdmin(MPTTModelAdmin):
    form = CategoryForm
    inlines = [CategoryCaracteristicInline]
    date_hierarchy = 'edited'
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ['editor']
    list_display = ['name', 'parent', 'edited', 'editor']
    list_filter = ['status', 'created','edited']
    search_fields = ['name', 'editor__username']
    mptt_level_indent = 30
    save_on_top = True
    list_select_related = ['editor'] 
    fieldsets = (
            (None, {
                'fields': (('name','slug',),)
            }),
            (None, {
                'fields': (('parent','status',), ('image','template_name'))
            }),
            (None, {
                'fields': (('description',),)
            }),
            )
    
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'editor', None) is None:
            obj.editor = request.user
        obj.save()


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    form = BrandForm
    date_hierarchy = 'edited'
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ['editor']
    list_display = ['name', 'image', 'status', 'editor','edited']
    list_filter = ['status', 'created','edited']
    search_fields = ['name', 'editor__username']
    list_select_related = ['editor']
    fieldsets = (
            (None, {
                'fields': (('name','slug',),)
            }),
            (None, {
                'fields': ('status','image',),
            }),
            )
    
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'editor', None) is None:
            obj.editor = request.user
        obj.save()