from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Repeat password',
        widget=forms.PasswordInput
    )
    
    class Meta:
        model = get_user_model()
        fields = ["username", "email"]
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']
    
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use')
        return data
    
    def save(self, commit=True):
        # Save the user instance without the password
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])  # Set password securely
        if commit:
            user.save()  # Save the user with the password hash
        return user
