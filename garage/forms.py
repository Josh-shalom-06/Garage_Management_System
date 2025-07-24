# garage/forms.py

from django import forms
from .models import Customer, Car, ServiceRecord, Mechanic, stock

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address']

class MechanicForm(forms.ModelForm):
    class Meta:
        model = Mechanic
        fields = ['name', 'email', 'phone', 'address','experience']        

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['customer', 'make', 'model', 'license_plate', 'year']

class ServiceRecordForm(forms.ModelForm):
    class Meta:
        model = ServiceRecord
        fields = ['car','mechanic', 'service_date', 'service_type', 'description','amount']
        widgets = {
            'service_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'service_type': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

#class stock_form(forms.ModelForm):
 #   class Meta:
  #      model = stock
   #     fields = ['partname','qty']

               
class stock_form(forms.ModelForm):
    class Meta:
        model = stock
        fields = ['partname', 'qty', 'price', 'supplier', 'restock_date', 'low_stock_threshold']
        widgets = {
            'restock_date': forms.DateInput(attrs={'type': 'date'}),}