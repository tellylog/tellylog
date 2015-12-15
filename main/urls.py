from django.conf.urls import url
from main.views import MainView
from . import views

app_name = 'main'
urlpatterns = [
    # url(r'^$', views.main, name='main'),
    url(r'^$', MainView.as_view(), name='main'),
    url(r'^aboutus/$', views.aboutus, name='aboutus'),
    url(r'^login/$', views.login, name='login'),
]
