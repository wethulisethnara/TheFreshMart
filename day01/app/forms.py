from django import forms
from .models import *


class CategoryForm(forms.ModelForm):
    class Meta:
        model = category
        fields = '__all__'  # or specify the fields you want to include
        
class UnitForm(forms.ModelForm):
    class Meta:
        model = unit
        fields = '__all__'
        
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'
        
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Your Name'
        }),
        label='Name'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Your Email'
        }),
        label='Email'
    )
    subject = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Subject'
        }),
        label='Subject'
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'placeholder': 'Your Message', 
            'rows': 5
        }),
        label='Message'
    )

class buy(forms.ModelForm): 
  class Meta: 
        model = Order 
        fields = ['customer', 'item', 'address', 'mobile', 'quantity'] 
        widgets = { 
            'customer': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter customer name'}), 
            'item': forms.CheckboxSelectMultiple(attrs={'class': 'input-field'}), 
            'address': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter delivery address'}), 
            'mobile': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter mobile number'}), 
            'quantity': forms.NumberInput(attrs={'class': 'input-field', 'placeholder': 'Enter quantity'}), 
        }