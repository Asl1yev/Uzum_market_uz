from django.urls import path
from .views import HomeView,CategoriesView,CategoryDetailView,ProductDetailView,\
    AddCategoryView,AddProductView,EditProductView,DeleteProductView,\
    SearchProductView
urlpatterns = [
    path('',HomeView,name='home'),
    path('category/',CategoriesView,name='cat'),
    path('addproduct/',AddProductView,name='addproduct'),
    path('addcategory/',AddCategoryView,name='addcategory'),
    path('search/',SearchProductView.as_view(),name='search'),
    path('editproduct/<slug:prod_slug>/',EditProductView,name='editproduct'),
    path('category/detail/<str:slug>/',CategoryDetailView,name='catdet'),
    path('product/delete/<str:prod_slug>/',DeleteProductView,name='delete'),
    path('product/<str:cat_slug>/<str:prod_slug>/',ProductDetailView,name='productdet'),

]