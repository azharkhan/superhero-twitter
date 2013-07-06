from django.db import models
from django.contrib.auth.models import User

# Defining the Tweet model

class Tweet(models.Model):
  content = models.CharField(max_length=140)
  user = models.ForeignKey(User)
  date_created = models.DateTimeField(auto_now=True, blank=True)

  def __unicode__(self):
    return self.content

# Profile Model - using django users model
# maps users to their followers and people they follow
# Symmetrical relationship turned off to allow one sided following

class UserProfile(models.Model):
  user = models.OneToOneField(User)
  follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)

# create profile when called from model using property
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
