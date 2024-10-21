from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Prénom')
    last_name = forms.CharField(max_length=30, required=True, label='Nom')
    email = forms.EmailField(max_length=254, required=True, label='Adresse e-mail')

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user =super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class CustomAuthentificationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')