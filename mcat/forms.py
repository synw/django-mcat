# -*- coding: utf-8 -*-

from django import forms


class FilterForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}))
    name.help_text = ''
    name.label = ''
    
    class Meta:
        fields = [ 'name']