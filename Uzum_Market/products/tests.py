from django.test import TestCase
from django.urls import reverse
from .forms import AddCategoryForm, AddProductForm
from .models import Category, Products
from django.contrib.auth.models import User

class TestAddCategoryView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_add_category_view(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('add_category'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'addcategory.html')

        form_data = {
            'slug': 'test-category',
            'name': 'Test Category',
            'description': 'Test description',
            'meta_title': 'Test Meta Title',
            'meta_keywords': 'Test Meta Keywords',
            'meta_description': 'Test Meta Description',
        }

        response = self.client.post(reverse('add_category'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.first().name, 'Test Category')

class TestAddProductView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(
            slug='test-category',
            name='Test Category',
            description='Test description',
            meta_title='Test Meta Title',
            meta_keywords='Test Meta Keywords',
            meta_description='Test Meta Description'
        )

    def test_add_product_view(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('add_product'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'addproduct.html')

        form_data = {
            'category': self.category.id,
            'slug': 'test-product',
            'name': 'Test Product',
            'small_description': 'Test Small Description',
            'quantity': 10,
            'description': 'Test description',
            'original_price': 100.0,
            'selling_price': 90.0,
            'status': True,
            'trending': True,
            'tag': 'Test Tag',
            'meta_title': 'Test Meta Title',
            'meta_keywords': 'Test Meta Keywords',
            'meta_description': 'Test Meta Description',
        }

        response = self.client.post(reverse('add_product'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(Products.objects.count(), 1)
        self.assertEqual(Products.objects.first().name, 'Test Product')

