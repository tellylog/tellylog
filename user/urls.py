from django.conf.urls import url
from . import views

app_name = 'user'
urlpatterns = [
    url(r'^sign-up/$', views.SignUp, name='sign_up'),
    url(r'^sign-in/$', views.SignIn, name='sign_in'),
    url(r'^logout/$', views.Logout, name='logout'),
    url(r'^profile/$', views.Profile.as_view(), name='profile'),
]
