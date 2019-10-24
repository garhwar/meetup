from django.conf.urls import url
from meetup_auth import views

app_name = 'meetup_auth'

urlpatterns = [
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.signin, name='login'),
    url(r'^logout/$', views.signout, name='logout'),
]
