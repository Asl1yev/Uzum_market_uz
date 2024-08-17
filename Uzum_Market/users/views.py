from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.shortcuts import render,redirect

from products.models import Products, Cart
from .forms import UserRegisterForm,UserLoginForm
from django.contrib.auth.hashers import make_password
from django.contrib import messages


def SignupView(request):
    form=UserRegisterForm()
    if request.method=='POST':
        form=UserRegisterForm(request.POST,files=request.FILES)
        if form.is_valid():
            user=form.save(commit=False)
            user.password=make_password(form.cleaned_data['password2'])
            user.save()
            messages.success(request,"Saytdan ro'yxatdan o'tdingiz ")
            return redirect('login')

    context={
        "form":form
    }
    return render(request,"registration/signup.html",context)


def LoginView(request):
    if request.user.is_authenticated:
        messages.warning(request,"Siz allaqachon saytga kirgansiz ")
        return redirect('home')
    else:
        if request.method=='POST':
            form=UserLoginForm(request.POST)
            if form.is_valid():
                username=form.cleaned_data['username']
                password=form.cleaned_data['password']
                user=authenticate(request,username=username,password=password)

                if user is not None:
                    login(request,user)
                    messages.success(request, " Saytga muvaffaqiyatli kirdingiz !!! ")
                    return redirect('cat')
                else:
                    form.add_error(None,"Notog'ri parol yoki username ")
        else:
            form=UserLoginForm()
        context={
            "form":form
        }

        return render(request,"registration/login.html",context)


def LogoutView(request):
    if request.user.is_authenticated:
        logout(request)
        messages.warning(request,"Saytdan chiqib ketdingiz ")
        return render(request,"registration/logout.html")



""""Mahsulotni har bir foydalanuvchi Savatga qo'shish uchun view"""



# views.py

from .forms import CartForm

# Add other imports

def add_to_cart(request, product_id):
    product = Products.objects.get(id=product_id)

    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            product_qty = form.cleaned_data['product_qty']
            cart, created = Cart.objects.get_or_create(user=request.user, product=product, defaults={'product_qty': product_qty})
            if not created:
                cart.product_qty += product_qty
                cart.save()
            messages.success(request, f"{product.name} mahsuloti savatchaga qo'shildi.")
            return redirect('view_cart')

    return redirect('view_cart')



# views.py


def view_cart(request):
    user_cart = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.selling_price * item.product_qty for item in user_cart)

    context = {
        'user_cart': user_cart,
        'total_price': total_price,
    }

    return render(request, 'cart.html', context)
