from django.urls import path
from .views import *


urlpatterns=[
    path("",dashoard),
    path("products/",ProductView.as_view(),name="products")
]