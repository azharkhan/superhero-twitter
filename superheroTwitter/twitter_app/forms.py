from django import forms
from twitter_app.models import Tweet, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class TweetForm(forms.ModelForm):
  content = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 4, 'class': 'field span12',}))

  class Meta:
    model = Tweet
    exclude = ('user',)

class NewUserForm(UserCreationForm):
  email = forms.EmailField(required=True)
  first_name = forms.CharField(required=True, max_length=30)
  last_name = forms.CharField(required=True, max_length=40)
  username = forms.CharField(required=True, max_length=20)
  password1 = forms.CharField(widget=forms.PasswordInput)
  password2 = forms.CharField(widget=forms.PasswordInput)

  class Meta:
    model = User
    fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']

class AuthenticateForm(AuthenticationForm):
  username = forms.CharField()
  password = forms.CharField(widget=forms.PasswordInput)