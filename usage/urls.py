from django.conf.urls import url

from usage import views

app_name = 'usage'
urlpatterns = [
    url(r'^register/$', views.user_registration, name = 'user-registration'),
    ]
