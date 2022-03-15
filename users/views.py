from unicodedata import decimal
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView
from users.serializers import CategorySerializer, ProductSerializer
from .models import *
from rest_framework.response import Response
import json
from django.core.paginator import Paginator
import datetime

@login_required
def dashoard(request):
    return render(request,"base.html")


        
class ProductView(APIView):
    template_name = 'dashboard.html'
    ctx = {}
    base_context = None
    ermission_classes = [IsAuthenticatedOrReadOnly]

    # main function of get document
    def get(self, request):
        self.data = request.GET
        if 'action' in self.data:
            action = int(self.data['action'])
            action_mapper = {1:self.get_product_list,2:self.get_category_list}
            status = action_mapper.get(action, lambda: 'Invalid')()
            if status == 'Invalid':
                self.ctx = {'status': 'error', 'msg': 'Invalid Action'}
            return Response(self.ctx)
        return self.base_context.render(request, self.template_name)
    def get_product_list(self):
        self.params = json.loads(self.data['params'])
        search = self.params['search']
        # self.offset = int(self.params['offset'])
        # self.limit = int(self.params.get('limit', 10))
        # self.page = int(self.offset / self.limit)
        products = Products.objects.all()
        if not search == "":
            products = products.filter(p_name__icontains=search)
        count = products.count()
        # products= Paginator(products, self.limit)
        # products= products.page(self.page + 1)

        arr = []

        for product in products:
            image = ImageList.objects.filter(product=product)
            if image.exists():
                new_dict = {
                    "image":f'<img src="{image.first().img}">',
                    "id":product.id,
                    'name': f'<a class="" style="cursor:pointer" data-id="{product.id}"><h4 class="p-0 m-0 text-bold text-secondary" ">' + product.p_name.title() + '</h4>' + '</a>',
                    'price':f'{product.price}',
                    'category':product.category.name,
                    "uploaded_on": datetime.datetime.strftime(product.timestamp, "%b %d,%Y"),
                    "action": f'<select class="form-control m-0 document-option" style="cursor:pointer" data-name="{product.p_name}" data-id="{product.id}"><option value="">Select Action </option><option value="2">Edit</option><option value="3">Make a Copy</option><option value="5">Preview</option><option class="text-danger" value="6">Delete</option></select>',
                }
            else:
                 new_dict = {
                    "image":f'<img src="https://picsum.photos/seed/picsum/200/300">',
                    "id":product.id,
                    'name': f'<a class="" style="cursor:pointer" data-id="{product.id}"><h4 class="p-0 m-0 text-bold text-secondary" ">' + product.p_name.title() + '</h4>' + '</a>',
                    'price':f'{product.price}',
                    'category':product.category.name,
                    "uploaded_on": datetime.datetime.strftime(product.timestamp, "%b %d,%Y"),
                    "action": f'<select class="form-control m-0 document-option" style="cursor:pointer" data-name="{product.p_name}" data-id="{product.id}"><option value="">Select Action </option><option value="2">Edit</option><option value="3">Make a Copy</option><option value="5">Preview</option><option class="text-danger" value="6">Delete</option></select>',
                }
            arr.append(new_dict)
        self.ctx.update({'data': arr, 'count': count})
    def get_category_list(self):
        category_list = Category.objects.all()
        serialize = CategorySerializer(category_list,many=True)
        self.ctx.update({"data":serialize.data,"count":category_list.count()})

    def post(self,request):
        self.data = request.POST
        if 'action' in self.data:
            action = int(self.data['action'])
            action_mapper = {1:self.create_product}
            status = action_mapper.get(action, lambda: 'Invalid')()
            if status == 'Invalid':
                self.ctx = {'status': 'error', 'msg': 'Invalid Action'}
            return Response(self.ctx)
        return self.base_context.render(request, self.template_name)
    def create_product(self):
        user = self.request.user
        category = int(self.data["category"])
        p_name = self.data["p_name"]
        price = float(self.data["price"])
        p_discription = self.data["p_discription"]
        category = Category.objects.get(pk=category)
        data_create = Products.objects.create(user=user,category=category,p_name=p_name,price=price,p_discription=p_discription)
        if data_create:
            return self.ctx.update({"status":"ok",'msg':'success'})

        



        
    

