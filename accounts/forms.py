from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Profile
from django_countries.fields import CountryField


alphanumeric = RegexValidator(r'^[a-z][a-z0-9_.]*$', 'Somente caracteres alfanuméricos minúsculos . _  são permitidos.')


class SignUpForm(UserCreationForm):
    username = forms.CharField(label='', max_length=30, validators=[alphanumeric], widget=forms.TextInput(
        attrs={'placeholder': 'Nome de usuário'}))
    email = forms.CharField(label='', max_length=254, required=True, widget=forms.EmailInput(attrs={'placeholder': 'Seu e-mail'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserUpdateForm(forms.ModelForm):
    avatar = forms.FileField(label="", widget=forms.FileInput)
    profile_cover = forms.FileField(label="", widget=forms.FileInput)
    location = CountryField(blank_label='(Selecione País)')
    url = forms.URLField(initial='http://', label_suffix='seu site',)
    facebook = forms.CharField(initial='https://www.facebook.com/', label_suffix='seuperfil', required=False)
    instagram = forms.CharField(initial='https://www.instagram.com/', label_suffix='seuperfil', required=False)
    you_tube = forms.CharField(initial='https://www.youtube.com/channel/', label_suffix='seuperfil', required=False)
    bio = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 2, 'placeholder': 'Descreva você.'}
        ),
        max_length=500,
        help_text='The max length of the text is 500.'
    )

    class Meta:
        model = Profile
        fields = ['avatar', 'profile_cover', 'first_name', 'last_name', 'bio', 'location', 'email', 'url', 'facebook',
                  'instagram', 'you_tube']
