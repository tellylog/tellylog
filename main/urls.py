from django.conf.urls import url
from . import views

app_name = 'main'
urlpatterns = [
    # url(r'^$', views.main, name='main'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    # url(r'^login/$', views.login, name='login'),
]
