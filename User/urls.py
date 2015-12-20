from django.conf.urls import url
from . import views

app_name = 'user'
urlpatterns = [
    url(r'^sign-up/$', views.SignUp, name='sign_up'),
]
