from django import forms
from .models import Products,Category

class AddCategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields="__all__"

class AddProductForm(forms.ModelForm):
    class Meta:
        model=Products
        fields="__all__"