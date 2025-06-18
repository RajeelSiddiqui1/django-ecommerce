from django import forms
from .models import SimpleUser, Order


#user registration form
class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = SimpleUser
        fields = ['name','email','password']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your name'}),
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter your email'}),
            'password': forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter your password'})
        }

# user login form 
class UserLoginForm(forms.Form):
     email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address_line1', 'address_line2', 
                 'city', 'state', 'postal_code', 'country']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'first_name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'last_name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'}),
            'address_line1': forms.TextInput(attrs={'class': 'form-control', 'id': 'address_line1'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control', 'id': 'address_line2'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'id': 'city'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'id': 'state'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'id': 'postal_code'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'id': 'country'}),
        }
        
        
       