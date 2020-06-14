
from django.shortcuts import render

# Create your views here.
from requests import Response
from rest_framework import viewsets, generics,permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView
from .serializers import *
from .models import *
from rest_framework.decorators import action
import datetime
from django.db.models import Q
import random

# class UserViewset(viewsets.ModelViewSet):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#
#     @action(methods=['get','POST'],detail=True)
#     def rigister_user(self,request,pk=None):
#
#         user=self.get_object()
#         user.objects=request.data
#         #user.add_time=datetime.datetime.strftime('%Y/%m/% %H:%M',datetime.datetime.now())
#         print(user)
#         user.save()
#         serializer=self.get_serializer(user)
#         return Response(serializer.data)
#
#     @action(methods=['get','put'],detail=True)
#     def change_password(self,request):
#         user=self.get_object()
#         user.password=request.data.get('password')
#         user.save()
#         serializer=self.get_serializer(UserSerializer)
#         return Response(serializer.data)

class GoodsDetail(generics.ListAPIView):
    #由商品id返回商品详细信息，无id返回全部商品信息
    serializer_class = GoodsDetailSerializer
    permission_classes = (permissions.AllowAny,)
    def get_queryset(self):
        goods_id=self.request.query_params.get('itemID',None)
        if goods_id is not None:
            queryset=Goods.objects.filter(id=goods_id)
            goods_obj=queryset.first()
            print(goods_obj)
            goods_obj.click+=1
            goods_obj.save()
        else:
            queryset=Goods.objects.all()
        return queryset

class GoodsListByCategory(generics.ListAPIView):
    #由分类id返回商品简略信息，无分类id返回所有简略信息
    serializer_class = GoodsSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (SearchFilter,OrderingFilter)
    search_fields=('detail')
    ordering_fields=('__all__')
    ordering=('-click')
    def get_queryset(self):
        category_id=self.request.query_params.get('category',None)

        if category_id is not None:
            queryset=Goods.objects.filter(category=Category.objects.filter(id=category_id).first())
        else:
            queryset=Goods.objects.all()
        return queryset


class GoodsSelect(generics.ListAPIView):
    #商品查询接口，商品名、简介模糊查询
    serializer_class = GoodsSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (SearchFilter,OrderingFilter)
    search_fields=('detail')
    ordering_fields=('__all__')
    ordering=('id')
    def get_queryset(self):
        keyword=self.request.query_params.get('keyword',None)
        if keyword is not None:
            queryset=Goods.objects.filter(Q(name__icontains=keyword)|Q(brief__icontains=keyword))
        else:
            queryset=Goods.objects.all()
        return queryset

class CategoryListView(generics.ListAPIView):
    #商品种类列表
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)

class UserCreateView(generics.CreateAPIView):
    #注册
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        print(self.request.data)
        name = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        mobile = serializer.validated_data.get('mobile')
        serializer.save(username=name,password=password,mobile=mobile)

class AddressListView(generics.ListAPIView):
    serializer_class = AddressSerializer
    permission_classes = (permissions.AllowAny,)
    def get_queryset(self):
        user_id=self.request.query_params.get('userID',None)
        if user_id is not None:
            queryset=Address.objects.filter(user=User.objects.filter(id=user_id).first())
        else:
            queryset=None
        return queryset

class ProfileRUView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (permissions.AllowAny,)
    def get_object(self):
        profile=Profile.objects.get(user=User.objects.get(id=self.request.query_params('id',None)))
        return profile

class LoginView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    def get_object(self):
        print(self.request.query_params)
        username=self.request.query_params.get('username',None)
        password=self.request.query_params.get('password',None)
        try:
            user=User.objects.get(username=username)
            if user.password==password:
                return user
            else:
                return None
        except:
            return None

class OrderCreatView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        print(self.request.data)
        user=serializer.validated_data.get('buyer')
        goods=serializer.validated_data.get('goods')
        message=serializer.validated_data.get('message')
        contact=serializer.validated_data.get('contact')
        address=serializer.validated_data.get('address')
        serializer.save(buyer=user,cost=goods.price,status='pending',order_sn=random.randint(100000,1000000),message=message,contact=contact,address=address)
        if goods.amount>=1:
            goods.amount-=1
        else:
            goods.amount=0
        goods.save()



