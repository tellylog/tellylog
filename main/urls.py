from django.conf.urls import url

from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^aboutus/$', views.aboutus, name='aboutus'),
    url(r'^login/$', views.login, name='login'),
]
