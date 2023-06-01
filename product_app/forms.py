from django import forms

from .models import *


class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = ['name', 'description', 'image']

class SubCategoryForm(forms.ModelForm):
	class Meta:
		model = Subcategory
		fields = ['name', 'category', 'description', 'image']
		widgets = {
            'category': forms.Select(attrs={'id': 'id_category'}),
            'name': forms.Select(attrs={'id': 'id_subcategory'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'brand', 'description', 'category', 'sub_category', 'mrp', 'image', 'sell_count', 'availability', 'stock']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control', 'id': 'category'}),
            'sub_category': forms.Select(attrs={'class': 'form-control', 'id': 'subcategory'}),
            'mrp': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'sell_count': forms.TextInput(attrs={'class': 'form-control'}),
            'availability': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'stock': forms.TextInput(attrs={'class': 'form-control'}),
        }
        def __init__(self, *args, **kwargs):
            super(ProductForm, self).__init__(*args, **kwargs)
            self.fields['category'].empty_label = 'Select a category'
            self.fields['sub_category'].empty_label = 'Select a subcategory'

class ExampleForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder' :'Email', 'class': 'form-control'}))