# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from codemirror2.widgets import CodeMirrorEditor
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from mcat.models import Product, ProductImage, ProductCaracteristic, CategoryCaracteristic, Category, Brand
from mcat.conf import CODE_MODE, USE_ADMIN_BOOTSTRAPED


#~ ========================================= Forms ==================================
 
class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'slug', 'status', 'image', 'editor']
        widgets = {'status': forms.RadioSelect}


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'parent', 'image', 'template_name', 'status', 'editor']
        widgets = {'status': forms.RadioSelect}
        
        
class ProductForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        if USE_ADMIN_BOOTSTRAPED:
            self.fields['description'].label = 'no label'
        
    class Meta:
        model = Product
        fields = ['name', 'slug', 'description', 'short_description', 'brand', 'category', 'status', 'editor', 'slideshow_type', 'slideshow_width', 'slideshow_height']
        description_widget = forms.Textarea(attrs={'style': 'width:100%;'})
        if CODE_MODE is True:
            description_widget = CodeMirrorEditor(options={
                                                             'mode':'htmlmixed',
                                                             'indentWithTabs':'true', 
                                                             'indentUnit' : '4',
                                                             'lineNumbers':'true',
                                                             'autofocus':'true',
                                                             #'highlightSelectionMatches': '{showToken: /\w/, annotateScrollbar: true}',
                                                             'styleActiveLine': 'true',
                                                             'autoCloseTags': 'true',
                                                             'keyMap':'vim',
                                                             'theme':'blackboard',
                                                             }, 
                                                             modes=['css', 'xml', 'javascript', 'htmlmixed'],
                                                    )
        else:
            description_widget = CKEditorUploadingWidget()
        short_description_widget = forms.Textarea(attrs={'style': 'min-width:100% !important;', 'rows':6, 'cols':80})
        widgets = {
                   'status': forms.RadioSelect,
                   'description': description_widget,
                   'short_description' : short_description_widget,
                   }
        
        
class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'order', 'product', 'status', 'editor']
        widgets = {'status': forms.RadioSelect}


class ProductCaracteristicInlineForm(forms.ModelForm):
        
    def __init__(self, *args, **kwargs):
        super(ProductCaracteristicInlineForm, self).__init__(*args, **kwargs)
        product = self.obj
        category = product.category
        caracteristics = CategoryCaracteristic.objects.filter(category=category)
        names = ()
        for carac in caracteristics:
            names += ((carac.slug, carac.name),)
        #self.fields['name'] = forms.ChoiceField(choices=names) 
        return

    class Meta:
        model = ProductCaracteristic
        fields = ['name', 'value']


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
    readonly_fields = ['editor']
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
            'fields': (('price', 'discounted_percentage'), 'discounted_price')
        }),
        (None, {
            'fields': (('status', 'short_description'), ('available', 'template_name'))
        }),
        (_(u'Slideshow options'), {
            'classes': ('collapse',),
            'fields': (('slideshow_type',), ('slideshow_width', 'slideshow_height') )
        }),
    )
    
    def form_valid(self, form):
        """This is what's called when the form is valid."""
        instance = form.save(commit=False)
        print "Form valid ----------------"
        return super(ProductAdmin, self).form_valid(form)
    
    def form_invalid(self, form):
        """This is what's called when the form is valid."""
        instance = form.save(commit=False)
        print "Form invalid ----------------"
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
        
"""
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
"""        
    
