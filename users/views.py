from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from users.serializers import ProductSerializer
from .models import *
@login_required
def dashoard(request):
    return render(request,"dashboard.html")

class ProductList(ListAPIView):
    queryset= Products.objects.all()
    serializer_class = ProductSerializer
        
class ProductManage(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user = request.user
        category = request.data["category"]
        
    

