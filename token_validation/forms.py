from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.urls import reverse_lazy
from .models import Account

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label = 'Password', widget = forms.PasswordInput)
    password2 = forms.CharField(label = 'Confirm Password', widget = forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'email', 'token', 'is_active', 'is_admin')
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2
    
    def save(self, commit = True):
        user = super().save(commit = False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label = ("Password"), 
    help_text=("Raw passwords are not stored, so there is no way to see " \
                    "this user's password, but you can change the password " \
                    "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'password', 'email', 'token', 'is_active', 'is_admin')
    
    def clean_password(self):
        return self.initial['password']

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    token_inp = forms.CharField(label="Book Token")
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'email', 'token_inp', 'password1', 'password2')

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if any(char.isdigit() for char in name):
            raise forms.ValidationError("Name cannot have numbers")
        return name

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not phone.isnumeric():
            raise forms.ValidationError("Phone number can have only numbers")
        return phone

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if len(password1) < 6:
            raise forms.ValidationError("Password too small")
        elif password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class PasswordChangeForm(forms.Form):
    previous_password = forms.CharField(min_length=6, label='Enter your old password', widget=forms.PasswordInput)
    password1 = forms.CharField(min_length=6, label='Enter new password', widget=forms.PasswordInput)
    password2 = forms.CharField(min_length=6, label='Confirm password', widget=forms.PasswordInput)

class SubscriptionForm(forms.Form):
    email = forms.EmailField(label='Enter your email', widget=forms.EmailInput)


class TokenUploadForm(forms.Form):
    csv = forms.FileField(label="Token CSV")

