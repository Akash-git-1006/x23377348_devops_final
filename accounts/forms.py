from django import forms
from .models import house
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


class AdForm(forms.ModelForm):
    # Explicitly define the number_of_bedrooms field with choices
    number_of_bedrooms = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 9)],  # Choices from 1 to 8
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Number of Bedrooms *"
    )

    number_of_bathrooms = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 9)],  # Choices from 1 to 8
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Number of Bathrooms *"
    )


    class Meta:
        model = house
        fields = (
           'property_type','description', 'location', 'rent', 'square_feet', 'number_of_bedrooms', 
            'number_of_bathrooms', 'phone_number', 'Available_from', 'image1', 'image2', 'image3'
        )
        exclude = ['seller']  # Exclude the seller field
        

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken. Please choose a different one.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        # Minimum length validation
        if len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        # Uppercase and lowercase validation
        if not any(char.isupper() for char in password1) or not any(char.islower() for char in password1):
            raise ValidationError("Password must contain both uppercase and lowercase letters.")

        # Special character validation
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            raise ValidationError("Password must contain at least one special character.")

        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # Check if passwords match
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match. Please enter the same password in both fields.")

        return cleaned_data
    
    
