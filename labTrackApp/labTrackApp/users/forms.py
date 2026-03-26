from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

UserModel = get_user_model()

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ("username", "email", "password1", "password2")
        
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ("username", "email", "role")
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if UserModel.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError('Email is already in use.')
        return email
