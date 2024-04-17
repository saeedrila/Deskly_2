from django import forms

from .models import *


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description", "image"]


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ["name", "category", "description", "image"]
        widgets = {
            "category": forms.Select(attrs={"id": "id_category"}),
            "name": forms.Select(attrs={"id": "id_subcategory"}),
        }


from multiupload.fields import MultiFileField


class ProductForm(forms.ModelForm):
    image_files = MultiFileField(
        label="Product Images",
        required=False,
        max_num=2,
        max_file_size=1024 * 1024 * 5,  # 5MB
        min_num=1,
    )

    class Meta:
        model = Product
        fields = [
            "name",
            "brand",
            "description",
            "category",
            "sub_category",
            "mrp",
            "sell_count",
            "availability",
            "stock",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "brand": forms.Select(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control", "id": "category"}),
            "sub_category": forms.Select(
                attrs={"class": "form-control", "id": "subcategory"}
            ),
            "mrp": forms.TextInput(attrs={"class": "form-control"}),
            "sell_count": forms.TextInput(attrs={"class": "form-control"}),
            "availability": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "stock": forms.TextInput(attrs={"class": "form-control"}),
        }

        def __init__(self, *args, **kwargs):
            super(ProductForm, self).__init__(*args, **kwargs)
            self.fields["category"].empty_label = "Select a category"
            self.fields["sub_category"].empty_label = "Select a subcategory"


class ExampleForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Name", "class": "form-control"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Email", "class": "form-control"})
    )


# Image cropping tool example
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("file",)
