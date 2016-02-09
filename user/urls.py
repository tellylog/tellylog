from django.conf.urls import url
from . import views

app_name = 'user'
urlpatterns = [
    url(r'^sign-up/$', views.SignUp.as_view(), name='sign_up'),
    url(r'^sign-in/$', views.SignIn, name='sign_in'),
    url(r'^logout/$', views.Logout, name='logout'),
    url(r'^profile/$', views.Profile.as_view(), name='profile'),
    # url(r'^pwforget/$', views.PWForget.as_view(), name='pwforget'),
    url(r'^password/reset/$', 'django.contrib.auth.views.password_reset',
    {'post_reset_redirect': '/user/password/reset/done/'}, name='password_reset'),
    url(r'^password/reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'django.contrib.auth.views.password_reset_confirm',  
    {'post_reset_redirect': '/user/password/done/'}, name='password_reset_token'),
    url(r'^password/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_done'),
]
