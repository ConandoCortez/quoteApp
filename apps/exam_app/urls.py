from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^quotes$', views.success),
    url(r'^addQuote$', views.add),
    url(r'^users/(?P<id>\d+)$', views.user),
    url(r'^favoriteQuote/(?P<id>\d+)$', views.favorites),
    url(r'logout$', views.logout),
]
