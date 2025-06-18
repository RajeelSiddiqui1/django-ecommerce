from django import forms
from .models import Admin, Category, Products

# admin signup
class AdminSignup(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['name', 'email', 'password']  # ✅ Correct spelling
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),  # ✅ Correct widget
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        }

# admin login
class AdminLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


# category form
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'photo']  
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Product Category Name'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }


# product form 
class ProductForm(forms.ModelForm):
    class Meta:
        model= Products
        fields= ['name','description','price','discount','sku','in_stock','categories','photos']
        widgets= {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter product description', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'sku': forms.NumberInput(attrs={'class': 'form-control'}),
            'in_stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'categories': forms.Select(attrs={'class': 'form-control'}),
            'photos': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'upload image'}),
        }


# blog status 
# class ProductStatusForm(forms.Form):
#     action = forms.ChoiceField(
#         choices=[
#             ('pending', 'Pending'),
#             ('approved', 'Approved'),
#         ],
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )