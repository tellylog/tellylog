from django.conf.urls import url
from . import views

app_name = 'main'
urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^about/$', views.About.as_view(), name='about'),
    url(r'^sign-in/$', views.SignIn.as_view(), name='sign_in'),
    url(r'^sign-up/$', views.SignUp.as_view(), name='sign_up'),
    url(r'^overview/$', views.Overview.as_view(), name='overview'),
]
