from django.db import models
from django.contrib.auth.hashers import make_password

# Admin
class Admin(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)
    email = models.EmailField(max_length=100, null=False)
    password = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


    def __str__(self):
        return f'name:{self.name}'        

# Category
class Category(models.Model):
    name = models.CharField(unique=True, null=False, max_length=100)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'name{self.name}'

# Product
class Products(models.Model):
    name = models.CharField( max_length=32, null=False)
    description = models.TextField( null=False)
    photos = models.ImageField(upload_to='photos/', null=False, blank=False)
    price = models.FloatField(null=False, max_length=20)
    discount = models.IntegerField(null=True)
    sku = models.IntegerField(null=True)
    in_stock = models.IntegerField(null=True)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'name{self.name} - category{self.categories}'
