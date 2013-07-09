from django.conf.urls import patterns, include, url
from twitter_app import views
from rest_framework import routers

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'tweets', views.TweetViewSet)
router.register(r'profiles', views.UserProfileViewSet)

urlpatterns = patterns('',
  url(r'^api/', include(router.urls)),
  url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
  url(r'^$', 'twitter_app.views.user_home'),
  url(r'^login$', 'twitter_app.views.login_view'),
  url(r'^logout$', 'twitter_app.views.logout_view'),
  url(r'^signup$', 'twitter_app.views.signup'),
  url(r'^submit$', 'twitter_app.views.submit'),
  url(r'^users/$', 'twitter_app.views.users'),
  url(r'^users/(?P<username>\w{0,30})/$', 'twitter_app.views.users'),
  url(r'^follow$', 'twitter_app.views.follow'),
  url(r'^unfollow$', 'twitter_app.views.unfollow'),
  url(r'^tweets$', 'twitter_app.views.all_tweets'),
    # Examples:
    # url(r'^$', 'superheroTwitter.views.home', name='home'),
    # url(r'^superheroTwitter/', include('superheroTwitter.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
