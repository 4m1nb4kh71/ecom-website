from django.forms import ModelForm
from .models import *
from django import forms



class ProductForm(ModelForm):
   
          
    class Meta:
        model = Product
        
        fields = '__all__'


       