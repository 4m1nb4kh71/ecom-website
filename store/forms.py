from django.forms import ModelForm
from .models import *
from django import forms



class ProductForm(ModelForm):
    def __init__(self, customer=None, *args, **kwargs):
        super(ProductForm, self).__init__(*args,**kwargs)
        if customer:
            self.fields['store'].queryset = Store.objects.filter(customer=customer)
            print(self.fields['store'].queryset)
    class Meta:
        model = Product
        widgets = {
            
            'store':forms.Select(attrs={'class':"form-control"}),
            'name':forms.TextInput(attrs={'class':"form-control"}),
            'price':forms.TextInput(attrs={'class':"form-control"}),
            'digital':forms.NullBooleanSelect(attrs={'class':"form-control"}),
            'description':forms.TextInput(attrs={'class':"form-control"}),
            'image':forms.FileInput(attrs={'class':"form-control"}),
            
        }

        fields = '__all__'
        
class StoreForm(ModelForm):
    def __init__(self, customer=None, *args, **kwargs):
        super(StoreForm, self).__init__(*args,**kwargs)
        if customer:
            self.fields['customer'].queryset = Customer.objects.filter(user=customer)
            print(self.fields['customer'].queryset)
    class Meta:
        model = Store
        widgets = {
            
            'storename':forms.TextInput(attrs={'style':'display:inline-block;'}),
            
            
        }
        fields = '__all__'
        
    
   