from django import forms
from django.contrib.contenttypes import fields
from django.db.models.base import Model

from .models import Order

class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_date'].label = 'Date of receipt of order'

    order_date = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}))
    
    class Meta:
        model = Order
        fields = (

             'first_name', 'last_name', 'phone', 'address', 'buying_type', 'order_date', 'comment'
        ) 