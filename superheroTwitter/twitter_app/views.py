from django.contrib.auth.models import User
from twitter_app.models import Tweet, UserProfile
from rest_framework import viewsets
from twitter_app.serializers import UserSerializer, TweetSerializer, UserProfileSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from twitter_app.forms import TweetForm, NewUserForm, AuthenticateForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer

class TweetViewSet(viewsets.ModelViewSet):
  queryset = Tweet.objects.all()
  serializer_class = TweetSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
  queryset = UserProfile.objects.all()
  serializer_class = UserProfileSerializer

def index(request, auth_form=None, user_form=None):
  if request.user.is_authenticated():
    tweet_form = TweetForm()
    user = request.user
    tweets_self = Tweet.objects.filter(user = user.id)
    tweets_friends = Tweet.objects.filter(user__userprofile__in = user.profile.follows.all)
    tweets = tweets_self | tweets_friends

    return render(request, 'tweets.html', {'tweet_form': tweet_form, 'user': user, 
                                              'tweets': tweets, 'next_url': '/'})
  else:
    auth_form = auth_form or AuthenticateForm()
    new_user_form = NewUserForm()

    return render(request, 'home.html', {'auth_form': auth_form, 
                                          'new_user_form': new_user_form})

def login_view(request):
  if request.method == 'POST':
    form = AuthenticateForm(data=request.POST)
    if form.is_valid():
      login(request, form.get_user())
      return redirect('/')
    else:
      return index(request, auth_form=form)
  return redirect('/')

def logout_view(request):
  logout(request)
  return redirect('/')

def signup(request):
  new_user_form = NewUserForm(data=request.POST)
  if request.method == 'POST':
    if new_user_form.is_valid():
      username = new_user_form.clean_username()
      password = new_user_form.clean_password2()
      new_user_form.save()
      user = authenticate(username=username, password=password)
      login(request, user)
      return redirect('/')
    else:
      return index(request, new_user_form=new_user_form)
  return redirect('/')

@login_required
def submit(request):
  if request.method == "POST":
    tweet_form = TweetForm(data=request.POST)
    next_url = request.POST.get("next_url", "/")
    if tweet_form.is_valid():
      tweet = tweet_form.save(commit=False)
      tweet.user = request.user
      tweet.save()
      return redirect(next_url)
    else:
      return public(request, tweet_form)
  return redirect('/')

@login_required
def public_tweets(request, tweet_form=None):
  tweet_form = tweet_form or TweetForm()
  tweets = Tweet.objects.all().reverse()
  return render(request, 'public.html', 
                {'tweet_form': tweet_form, 'next_url': '/tweets', 
                'tweets': tweets, 'username': request.user.username})

# get latest tweets
def get_latest(user):
  try:
    return user.tweet_set.order_by('-id')[0]
  except IndexError:
    return ""

@login_required
def users(request, username="", tweet_form=None):
  if username:
    try: # get user if exists
      user = User.objects.get(username=username)
    except User.DoesNotExist:
      raise Http404
    tweets = Tweet.objects.filter(user=user.id) # get tweets from user
    if username == request.user.username or request.user.profile.follows.filter(user__username=username):
      return render(request, 'user.html', {'user': user, 'tweets': tweets})
    return render(request, 'user.html', {'user': user, 'tweets': tweets, 'follow':True})

  users = User.objects.all().annotate(tweet_count=Count('tweet'))
  tweets = map(get_latest, users)
  obj = zip(users, tweets)
  tweet_form = tweet_form or TweetForm()
  return render(request, 'profiles.html', {'obj':obj, 'next_url': '/users', 
                                            'tweet_form': tweet_form,
                                            'username': request.user.username })

@login_required
def follow(request):
  if request.method == "POST":
    follow_id = request.POST.get('follow', False)
    if follow_id:
      try:
        user = User.objects.get(id=follow_id)
        request.user.profile.follows.add(user.profile)
      except ObjectDoesNotExist:
        return redirect('/users')
    return redirect('/users')