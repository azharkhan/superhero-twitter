from django.contrib.auth.models import User
from twitter_app.models import Tweet, UserProfile
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ('url', 'username', 'email')

class TweetSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Tweet
    fields = ('content', 'user', 'date_created')

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = UserProfile
    fields = ('user', 'follows', 'followed_by')