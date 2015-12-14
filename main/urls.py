from django.conf.urls import url

from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.Main, name='main'),
    url(r'^aboutUs/$', views.AboutUs, name='aboutUs'),
    url(r'^logIn/$', views.logIn, name='logIn'),
]
