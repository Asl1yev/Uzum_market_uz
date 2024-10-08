from django import  forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(forms.ModelForm):
    password1=forms.CharField(label="Parol kiriting",widget=forms.PasswordInput)
    password2=forms.CharField(label="Parolni qayta kiriting",widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=('username','email','password1','password2')

    def clean_password2(self):
        password1=self.cleaned_data.get("password1")
        password2=self.cleaned_data.get("password2")

        if  password1 and password2 and password1 != password2:
            raise ValidationError("Kiritilgan parollar bir biriga mos bo'lishi kerak")
        return password1




class UserLoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Parol", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = User.objects.filter(username=username).first()

            if user is None or not user.check_password(password):
                raise ValidationError("Noto'g'ri foydalanuvchi nomi yoki parol")

        return cleaned_data




from django import forms

class CartForm(forms.Form):
    product_qty = forms.IntegerField(min_value=1)
