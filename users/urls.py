from django.urls import path
from .views import *


urlpatterns=[
    path("",dashoard),
    path("products/",ProductList.as_view(),name="products")
]