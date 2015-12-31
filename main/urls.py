from django.conf.urls import url
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

app_name = 'main'
urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^about/$', views.About.as_view(), name='about'),
    # url(r'^overview/$', views.Overview.as_view(), name='overview'),
    url(r'^overview/$', login_required(
        TemplateView.as_view(template_name='main/overview.html')), name='overview'),
]
