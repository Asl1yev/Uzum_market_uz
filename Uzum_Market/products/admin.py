from django.contrib import admin
from .models import Products,Category,Cart
from django.contrib.auth.models import Group

admin.site.register(Products)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.unregister(Group)


