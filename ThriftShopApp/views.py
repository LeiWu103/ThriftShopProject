from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from requests import Response
from rest_framework import viewsets, generics, permissions, response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListCreateAPIView
from .serializers import *
from .models import *
from rest_framework.decorators import action
import datetime
from django.db.models import Q
import random
from drf_multiple_model.views import ObjectMultipleModelAPIView


class GoodsDetail(generics.ListAPIView):
    '''
    由商品id返回商品详细信息
    无id返回全部商品信息
    '''
    serializer_class = GoodsDetailSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        goods_id = self.request.query_params.get('itemID', None)
        if goods_id is not None:
            queryset = Goods.objects.filter(id=goods_id)
            goods_obj = queryset.first()
            print(goods_obj)
            goods_obj.click += 1
            goods_obj.save()
        else:
            queryset = Goods.objects.all()
        return queryset


class GoodsListByCategory(generics.ListAPIView):
    '''
    由分类id返回商品简略信息
    无分类id返回所有简略信息
    '''
    serializer_class = GoodsSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('detail')
    ordering_fields = ('__all__')
    ordering = ('-click')

    def get_queryset(self):
        category_id = self.request.query_params.get('category', None)

        if category_id is not None:
            queryset = Goods.objects.filter(category=Category.objects.filter(id=category_id).first())
        else:
            queryset = Goods.objects.all()
        return queryset


class GoodsSelect(generics.ListAPIView):
    '''
    商品查询接口，由商品名、简介模糊查询
    '''
    serializer_class = GoodsSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('detail')
    ordering_fields = ('__all__')
    ordering = ('id')

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword', None)
        if keyword is not None:
            queryset = Goods.objects.filter(Q(name__icontains=keyword) | Q(brief__icontains=keyword))
        else:
            queryset = Goods.objects.all()
        return queryset


class CategoryListView(generics.ListAPIView):
    '''商品种类列表'''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)


class UserCreateView(generics.CreateAPIView):
    '''用户注册'''
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        print(self.request.data)
        name = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        mobile = serializer.validated_data.get('mobile')
        serializer.save(username=name, password=password, mobile=mobile)


class AddressListView(generics.ListAPIView):
    '''
    地址列表
    用户id查询地址表
    '''
    serializer_class = AddressSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        user_id = self.request.query_params.get('userID', None)
        if user_id is not None:
            queryset = Address.objects.filter(user=User.objects.filter(id=user_id).first())
        else:
            queryset = None
        return queryset


class ProfileRUView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (permissions.AllowAny,)

    def get_object(self):
        profile = Profile.objects.get(user=User.objects.get(id=self.request.query_params('id', None)))
        return profile


class LoginView(generics.RetrieveAPIView):
    '''
    登录验证
    正确则返回唯一用户id和用户名
    否则返回空
    '''
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def get_object(self):
        print(self.request.query_params)
        username = self.request.query_params.get('username', None)
        password = self.request.query_params.get('password', None)
        try:
            user = User.objects.get(username=username)
            if user.password == password:
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
        '''
        :param serializer:
        :return:
        '''
        print(self.request.data)
        user = serializer.validated_data.get('buyer')
        goods = serializer.validated_data.get('goods')
        message = serializer.validated_data.get('message')
        contact = serializer.validated_data.get('contact')
        address = serializer.validated_data.get('address')
        serializer.save(buyer=user, cost=goods.price, status='pending', order_sn=random.randint(100000, 1000000),
                        message=message, contact=contact, address=address)
        if goods.amount >= 1:
            goods.amount -= 1
        else:
            goods.amount = 0
        goods.save()


class MySellGoodsList(generics.ListAPIView):
    '''
    接受用户id,返回上架商品列表
    按时间排序
    '''
    serializer_class = GoodsSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('detail')
    ordering_fields = ('__all__')
    ordering = ('-add_time')

    def get_queryset(self):
        '''
        :return: 返回上架商品的查询集
        '''
        user_id = self.request.query_params.get('id', None)
        if user_id is not None:
            queryset = Goods.objects.filter(seller_id=user_id)
        else:
            queryset = Goods.objects.all()
        return queryset

class MyBuyGoodsList(generics.ListAPIView):
    '''
    根据用户id查询订单表
    返回购买成功的商品
    按订单生成时间排序
    '''
    serializer_class = GoodsSerializer
    permission_classes = (permissions.AllowAny,)


    def get_queryset(self):
        '''
        :return: 返回购买商品的查询集
        '''
        user_id = self.request.query_params.get('id', None)
        if user_id is not None:
            orders = Order.objects.filter(buyer_id=user_id, status="pending")
            l=list()
            for o in orders:
                l.append(o.goods)
            queryset = l
        else:
            queryset = None
        return queryset
