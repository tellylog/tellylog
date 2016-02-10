from django.conf.urls import url
from . import views

app_name = 'main'
urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^about/$', views.About.as_view(), name='about'),
    url(r'^overview/$', views.Overview.as_view(), name='overview'),
    url(r'^dummy/$', views.Dummy.as_view(), name='dummy'),
    url(r'^sign-in/$', views.SignIn.as_view(), name='signin'),
    url(r'^contact/$', views.Contact.as_view(), name='contact'),
    url(r'^help/$', views.Help.as_view(), name='help'),
]
