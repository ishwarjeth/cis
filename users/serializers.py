from rest_framework.serializers import ModelSerializer
from .models import *

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        