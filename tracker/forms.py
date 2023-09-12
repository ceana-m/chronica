from django import forms
from django.forms import ModelForm
from .models import List

class NewList(ModelForm):
    class Meta:
        model = List
        fields = '__all__'
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for item in self.visible_fields():
            item.label = ""
            item.field.widget.attrs['class'] = 'form-control'
            item.field.widget.attrs['placeholder'] = item.field.label