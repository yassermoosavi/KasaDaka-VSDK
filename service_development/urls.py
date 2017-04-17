from django.conf.urls import url

from . import views

app_name= 'service_development'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^choice/(?P<element_id>[0-9]+)/(?P<session_id>[0-9]+)$', views.choice, name='choice'),
    url(r'^register/$', views.user_registration, name = 'user-registration'),
]

