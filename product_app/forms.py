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
        fields = ['name', 'brand', 'description', 'category', 'sub_category', 'mrp', 'image', 'availability', 'stock']
        widgets = {
            'category': forms.Select(attrs={'id': 'id_category'}),
            'sub_category': forms.Select(attrs={'id': 'id_subcategory'}),
        }
