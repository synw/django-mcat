# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from mcat.models import Product, ProductImage, Category, Brand


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    
    
class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'slug', 'status', 'image', 'editor']
        widgets = {'status': forms.RadioSelect}


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'parent', 'image', 'status', 'editor']
        widgets = {'status': forms.RadioSelect}
        
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'description', 'short_description', 'brand', 'category', 'status', 'editor']
        widgets = {'status': forms.RadioSelect}
        
        
class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'order', 'product', 'status', 'editor']
        widgets = {'status': forms.RadioSelect}
        
        
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    inlines = [ProductImageInline]
    date_hierarchy = 'edited'
    raw_id_fields = ['category','brand']
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name','brand', 'price', 'category','upc','created','status','editor']
    list_filter = ['status', 'created','edited']
    search_fields = ['name','upc','brand__name','category__name','editor__username']
    list_select_related = ['editor','brand','category']
    readonly_fields = ['editor']
    save_on_top = True
    fieldsets = (
        (None, {
            'fields': (('name', 'slug'), ('category', 'brand'), ('navimage', 'upc'))
        }),
        (None, {
            'fields': (('price', 'discounted_percentage'), 'discounted_price')
        }),
        ("Description du produit", {
            'classes': ('collapse',),
            'fields': ('short_description', 'description')
        }),
        (None, {
            'fields': ('status',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'editor', None) is None:
            obj.editor = request.user
        obj.save()
        
        
@admin.register(Category)    
class CategoryAdmin(MPTTModelAdmin):
    form = CategoryForm
    date_hierarchy = 'edited'
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ['editor']
    list_display = ['name', 'parent', 'edited', 'editor']
    list_filter = ['status', 'created','edited']
    search_fields = ['name', 'editor__username']
    mptt_level_indent = 30
    actions_on_top = True
    list_select_related = ['editor'] 
    fieldsets = (
            (None, {
                'fields': (('name','slug',),)
            }),
            (None, {
                'fields': (('parent','status',), 'image')
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
        

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    form = ProductImageForm
    date_hierarchy = 'edited'
    readonly_fields = ['editor']
    list_display = ['product', 'image', 'status', 'editor', 'edited']
    list_filter = ['status', 'created','edited']
    search_fields = ['product__name', 'editor__username']
    list_select_related = ['editor']
    raw_id_fields = ['product']
    fieldsets = (
            (None, {
                'fields': (('product','status',), 'image','order')
            }),
            )
    
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'editor', None) is None:
            obj.editor = request.user
        obj.save()
        
    
