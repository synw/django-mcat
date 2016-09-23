# -*- coding: utf-8 -*-

from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from codemirror2.widgets import CodeMirrorEditor
from mptt.forms import TreeNodeChoiceField
from mcat.models import Product, ProductCaracteristic, CategoryCaracteristic, Category, Brand
from mcat.conf import CODE_MODE


class FilterForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}))
    name.help_text = ''
    name.label = ''
    
    class Meta:
        fields = [ 'name']
        
class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'slug', 'status', 'image', 'editor']
        widgets = {'status': forms.RadioSelect}


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'parent', 'image', 'template_name', 'status', 'editor']
        widgets = {'status': forms.RadioSelect, 'description': CKEditorUploadingWidget(config_name='mcat')}
        
        
class ProductForm(forms.ModelForm):
    upc = forms.CharField()
    upc.required = False
    category = TreeNodeChoiceField(queryset=Category.objects.all())
        
    class Meta:
        model = Product
        exclude = ['created', 'edited', 'editor']
        description_widget = forms.Textarea(attrs={'style': 'width:100%;'})
        if CODE_MODE is True:
            description_widget = CodeMirrorEditor(options={
                                                             'mode':'htmlmixed',
                                                             'indentWithTabs':'true', 
                                                             'indentUnit' : '4',
                                                             #'lineNumbers':'false',
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
            description_widget = CKEditorUploadingWidget(config_name='mcat')
        short_description_widget = forms.Textarea(attrs={'style': 'min-width:100% !important;', 'rows':6, 'cols':80})
        widgets = {
                   'status': forms.RadioSelect,
                   'description': description_widget,
                   'short_description' : short_description_widget,
                   'deal_conditions' : description_widget,
                   'deal_description' : description_widget,
                   
                   }

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