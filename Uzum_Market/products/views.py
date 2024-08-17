from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView

from .models import Category,Products
from django.contrib import messages
from .forms import AddProductForm,AddCategoryForm


def HomeView(request):
    category=Category.objects.all()
    products=Products.objects.all()
    context={
        'category':category,
        'products':products
    }
    return render(request,'home.html',context)

@login_required(login_url='login')
def CategoriesView(request):
    categories=Category.objects.filter(status=0)
    context={
        'categories':categories
    }
    return render(request,'categories.html',context)

@login_required(login_url='login')
def CategoryDetailView(request,slug):
    if (Category.objects.filter(slug=slug,status=0)):
        products=Products.objects.filter(category__slug=slug)
        category_name=Category.objects.filter(slug=slug).first()
        context={
            'products':products,
            'category_name':category_name
        }
        return render(request,"products.html",context)
    else:
        messages.warning(request,"Bu kategoriyada hozircha tovar yo'q")
        return redirect('cat')


def ProductDetailView(request,cat_slug,prod_slug):
    category=get_object_or_404(Category,slug=cat_slug,status=0)
    product=get_object_or_404(Products,category=category,slug=prod_slug)

    context={
        'product':product,
    }

    return render(request,"productdetail.html",context)


"""Kategoriya qo'shish uchun view"""
def AddCategoryView(request):
    form=AddCategoryForm()
    if request.method=='POST':
        form=AddCategoryForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Kategoriya qo'shildi")
            return redirect('cat')
    context={
        'form':form
    }
    return render(request,"addcategory.html",context)


"""Mahsulot  qo'shish uchun view"""

def AddProductView(request):
    form=AddProductForm()
    if request.method=='POST':
        form=AddProductForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Kategoriya qo'shildi")
            return redirect('cat')
    context={
        'form':form
    }
    return render(request,"addproduct.html",context)


"""Mahsulotni o'zgartirish"""

def EditProductView(request,prod_slug):
    product=get_object_or_404(Products,slug=prod_slug)
    form=AddProductForm(instance=product)
    if request.method=='POST':
        form=AddProductForm(request.POST,files=request.FILES,instance=product)
        if form.is_valid():
            form.save()
            messages.success(request,"Mahsulot tahrirlandi !!!")
            return redirect('cat')
    context={
        'form':form
    }
    return render(request,"editproduct.html",context)



"""Mahsulotni o'chirish"""
def DeleteProductView(request, prod_slug):
    product = get_object_or_404(Products, slug=prod_slug)

    if request.method == 'POST':
        product.delete()
        messages.success(request, "Mahsulot o'chirildi")
        return redirect('cat')

    context = {
        'product': product  # Shunday bo'lsa, sizga undagi ma'lumotlar kerak bo'ladi
    }

    return render(request, "deleteproduct.html", context)



"""Mahsulotlarni qidirish uchun View"""

class SearchProductView(ListView):
    model = Products
    template_name = "search_product.html"
    context_object_name = "products"

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Products.objects.filter(
            Q(name__icontains=query)|Q(trending__icontains=query)
            )
        else:
            return Products.objects.none()







