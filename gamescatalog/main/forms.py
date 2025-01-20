from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, CharField, EmailField, PasswordInput, EmailInput, ModelForm


class RegisterUserForm(UserCreationForm):
    username = CharField(widget=TextInput(attrs={'class': 'form-control','placeholder': 'Імʼя користувача'}))
    email = EmailField(widget=EmailInput(attrs={'class': 'form-control', 'placeholder': 'Електронна пошта'}))
    password1 = CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))
    password2 = CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторити пароль'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginUserForm(AuthenticationForm):
    username = CharField(widget=TextInput(attrs={'class': 'form-control','placeholder': 'Імʼя користувача'}))
    password = CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))


class ProfileUserForm(ModelForm):
    username = CharField(disabled=True, label='Логін', widget=TextInput(attrs={'class': 'form-control'}))
    email = EmailField(label='E-mail', widget=TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'first_name': 'Імʼя',
            'last_name': 'Прізвище',
        }
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
        }

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = CharField(label="Старий пароль", widget=PasswordInput(attrs={'class': 'form-control'}),)
    new_password1 = CharField(label="Новий пароль", widget=PasswordInput(attrs={'class': 'form-control'}),)
    new_password2 = CharField(label="Підтвердження пароля", widget=PasswordInput(attrs={'class': 'form-control'}),)
