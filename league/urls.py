from league.views import MyAccessUrl
from django.urls import path, include

urlpatterns = [
    path(r'', MyAccessUrl.as_view(), name='my-view')
]