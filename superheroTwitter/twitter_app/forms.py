from django import forms
from twitter_app.models import Tweet, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class TweetForm(forms.ModelForm):
  content = forms.CharField(required=True, label='', widget=forms.Textarea(attrs={
                                              'rows': 4, 
                                              'class': 'field span12',
                                              'placeholder': 'Enter Tweet Here...',}))

  class Meta:
    model = Tweet
    exclude = ('user',)

class NewUserForm(UserCreationForm):
  email = forms.EmailField(required=True)
  first_name = forms.CharField(required=True, max_length=30)
  last_name = forms.CharField(required=True, max_length=40)

  class Meta:
    model = User
    fields = ['email', 'first_name', 'last_name', 'username',]

class AuthenticateForm(AuthenticationForm):
  username = forms.CharField()
  password = forms.CharField(widget=forms.PasswordInput)