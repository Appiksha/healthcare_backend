from django.urls import path
from .views import *


urlpatterns = [
    path('guest/sos/',
         sosView.as_view(), name='guest sos'),
    path('guest/cood/',
         updateView.as_view(), name='guest sos cood update')
]
