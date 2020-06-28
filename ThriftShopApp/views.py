import data as data
from django.views.decorators.csrf import csrf_exempt
from requests import Response
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, parser_classes, authentication_classes, permission_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import parser_classes
from django.views.decorators.csrf import csrf_exempt  # 不进行csrf验证

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import base64, os
from django.core.files.base import ContentFile

from .serializers import *
from .models import *
from django.db.models import Q
import random


class GoodsDetail(generics.ListAPIView):
    """
    由商品id返回商品详细信息
    无id返回全部商品信息
    """
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
    """
    由分类id返回商品简略信息
    无分类id返回所有简略信息
    """
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
    """
    商品查询接口，由商品名、简介模糊查询
    """
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
    """商品种类列表"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)


class UserCreateView(generics.CreateAPIView):
    """用户注册"""
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        print(self.request.data)
        name = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        mobile = serializer.validated_data.get('mobile')
        account = str(10000 + User.objects.count()+1)
        serializer.save(username=name, password=password, mobile=mobile, account=account)
        profile = Profile(user=User.objects.get(account=account))
        profile.save()


class AddressListView(generics.ListAPIView):
    """
    地址列表
    用户id查询地址表
    """
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
    """
    Profile表的查询
    按外键user的id
    """
    serializer_class = ProfileSerializer
    permission_classes = (permissions.AllowAny,)

    def get_object(self):
        try:
            profile = Profile.objects.get(user_id=self.request.query_params.get('id', None))
        except:
            profile = None
        return profile


class ProfileEdit(generics.RetrieveUpdateAPIView):
    """
    Profile表的修改
    get
    """
    serializer_class = ProfileSerializer
    permission_classes = (permissions.AllowAny,)

    def get_object(self):
        try:
            print(self.request.query_params)
            profile = Profile.objects.get(user_id=self.request.query_params.get('userID', None))
            username = self.request.query_params.get('username', None)
            bio = self.request.query_params.get('bio', None)
            email = self.request.query_params.get('email', None)
            profile.user.username = username
            profile.user.save()
            profile.bio = bio
            profile.email = email
            profile.save()
        except:
            profile = None
        return profile


class LoginView(generics.RetrieveAPIView):
    """
    登录验证
    正确则返回唯一用户id和用户名
    否则返回空
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def get_object(self):
        print(self.request.query_params)
        username = self.request.query_params.get('account', None)
        password = self.request.query_params.get('password', None)
        try:
            user = User.objects.get(account=username)
            if user.password == password:
                return user
            else:
                return None
        except:
            return None


class OrderCreatView(generics.CreateAPIView):
    """创建订单"""
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        """
        :param serializer:
        :return:
        """
        print(self.request.data)
        user = serializer.validated_data.get('buyer')
        goods = serializer.validated_data.get('goods')
        message = serializer.validated_data.get('message')
        contact = serializer.validated_data.get('contact')
        address = serializer.validated_data.get('address')
        serializer.save(buyer=user, cost=goods.price, status='待处理', order_sn=random.randint(100000, 1000000),
                        message=message, contact=contact, address=address)
        if goods.amount >= 1:
            goods.amount -= 1
        else:
            goods.amount = 0
        goods.save()


class MySellGoodsList(generics.ListAPIView):
    """
    接受用户id,返回上架商品列表
    按时间排序
    """
    serializer_class = GoodsSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('detail')
    ordering_fields = ('__all__')
    ordering = ('-add_time')

    def get_queryset(self):
        """
        :return: 返回上架商品的查询集
        """
        user_id = self.request.query_params.get('userID', None)
        if user_id is not None:
            queryset = Goods.objects.filter(seller_id=user_id)
        else:
            queryset = Goods.objects.all()
        return queryset


class MyBuyGoodsList(generics.ListAPIView):
    """
    根据用户id查询订单表
    返回购买成功的商品
    按订单生成时间排序
    """
    serializer_class = OrderSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        """
        :return: 返回购买商品的查询集
        """
        user_id = self.request.query_params.get('buyerID', None)
        if user_id is not None:
            orders = Order.objects.filter(buyer_id=user_id)
            queryset = orders
        else:
            queryset = None
        return queryset


class ChangePassword(generics.RetrieveAPIView):
    """
    修改密码功能
    接受用户id、原密码、新密码和确认密码
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def get_object(self):
        id = self.request.query_params.get('userID', None)
        old = self.request.query_params.get('oldpassword', None)
        new = self.request.query_params.get('newpassword', None)
        try:
            user = User.objects.get(id=id)
            if user.password == old:
                user.password = new
                user.save()
                return user
            else:
                return None
        except:
            return None


class AddressCreate(generics.CreateAPIView):
    """新建地址"""
    serializer_class = AddressSerializer1
    permission_classes = (permissions.AllowAny,)
    queryset = Address.objects.all()

    def perform_create(self, serializer):
        user = serializer.validated_data.get('user')
        signer = serializer.validated_data.get('signer')
        location = serializer.validated_data.get('location')
        mobile = serializer.validated_data.get('mobile')
        serializer.save(user=user, signer=signer, location=location, mobile=mobile)


class AddressRUD(generics.RetrieveUpdateDestroyAPIView):
    """地址修改"""
    serializer_class = AddressSerializer1
    permission_classes = (permissions.AllowAny,)

    def get_object(self):
        id = self.kwargs['pk']
        obj = Address.objects.get(id=id)
        return obj

    def perform_update(self, serializer):
        serializer.save()


class GoodsCreate(generics.CreateAPIView):
    """上传商品"""
    serializer_class = GoodsCreateSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Goods.objects.all()

    def perform_create(self, serializer):
        print(serializer.validated_data)
        name = serializer.validated_data.get('name')
        amount = serializer.validated_data.get('amount')
        price = serializer.validated_data.get('price')
        brief = serializer.validated_data.get('brief')
        code = serializer.validated_data.get('code')
        image_str = str(code)
        image_str = image_str.split(',')[1]
        image_name = 'media/images/' + str(random.randint(1, 100000000)) + '.png'
        with open(image_name, 'wb') as f:
            f.write(base64.b64decode(image_str))
        image_name = image_name[6:100]
        transaction = serializer.validated_data.get('transaction')

        postage = serializer.validated_data.get('postage')
        category = serializer.validated_data.get('category')
        seller = serializer.validated_data.get('seller')
        serializer.save(name=name, amount=amount, click=0, price=price, brief=brief, image=image_name,
                        transaction=transaction, postage=postage, category=category, seller=seller, code=code)
        print(serializer)


# class ImageUpload(generics.CreateAPIView):
#     serializer_class = ImageUploadSerializer
#     permission_classes = (permissions.AllowAny,)
#     queryset = Image.objects.all()
#     def perform_create(self, serializer):
#         print(1)
#         img=serializer.validated_data.get('image')
#         print(img)
#         serializer.save(image=img)


class OrderList(generics.ListAPIView):
    """
    订单列表
    """
    serializer_class = OrderSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        sell_id = self.request.query_params.get('sellID', None)
        queryset = Order.objects.filter(goods__seller_id=sell_id)
        return queryset


class OrderDetail(generics.RetrieveAPIView):
    """订单详情"""
    serializer_class = OrderSerializer
    permission_classes = (permissions.AllowAny,)

    def get_object(self):
        order_id = self.request.query_params.get('orderID', None)
        obj = Order.objects.get(id=order_id)
        return obj


class OrderRUD(generics.RetrieveUpdateDestroyAPIView):
    """
    以pk判断
    订单详细信息和修改、删除操作
    """
    serializer_class = OrderRUDSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Order.objects.all()

    def get_object(self):
        order_id = self.kwargs['pk']
        obj = Order.objects.get(id=order_id)
        return obj

    def perform_update(self, serializer):
        op = self.request.query_params.get('operation', None)
        print(op)
        if op == "finish":
            serializer.save(status="已完成")
        elif op == "cancel":
            obj = Order.objects.get(id=self.kwargs['pk'])
            obj.goods.amount += 1
            obj.goods.save()
            serializer.save(status="已取消")

    def perform_destroy(self, instance):
        obj = Order.objects.get(id=self.kwargs['pk'])
        obj.goods.amount += 1
        obj.goods.save()
        instance.delete()


class ImageUpload(generics.CreateAPIView):
    serializer_class = ImageUploadSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Image.objects.all()

    def perform_create(self, serializer):
        image_str = str(serializer.validated_data.get('image'))
        print(image_str)
        image_str = image_str.split(',')[1]
        image_name = 'media/images/' + str(random.randint(1, 100000000)) + '.png'
        with open(image_name, 'wb') as f:
            f.write(base64.b64decode(image_str))

        serializer.save(image=image_name)


class GoodsRUD(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GoodsSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Goods.objects.all()
    # with open("C:\\Users\\wonai\\Desktop\\1.jpg", "rb") as f:  # 转为二进制格式
    #     base64_data = base64.b64encode(f.read())  # 使用base64进行加密
    #     print(base64_data)
    #     file = open('E:\\qq文件\img.txt', 'wt')  # 写成文本格式
    #     file.write(base64_data)
    #     file.close()
    # with open("E:\\qq文件\img.txt", "r") as f:
    #     # str = "iVBORw0KGgoAAAANSUhEUgAAANwAAAAoCAIAAAAaOwPZAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAQuSURBVHhe7ZptmoMgDIR7rh6o5+lpvEwP01XUGshAokgX+8z+7PKRTF6SoN7e/KMCnSlw68wemkMF3oSSEHSnAKHsLiQ0iFCSge4UIJTdhYQGEUoy0J0ChLK7kNAgQkkGulOAUHYXEhpEKMlAdwpcG8rhcRv/HkN3stIgW4F88DYoX89nObjmANuOc0eMXpHHcyX9+mowhgHKmdlChM0BZzvzet6DSSW7xjEWk8Hu+/O1x7zF1237/Uu4t/O46V6sZuARoZb9KqbO7On4rJlykqcYYnNAjSbx3Gmrj6WTzxirVlA+90F82G+nm4fX3zOxgqyKqRaUU7b8FpRDOeyjJa7k5oByT1yWse4mxfDC3NrrprnQtQeUMuUXoURmCGHdKfl/oTS8MElxu2mudO0BXUCZL8efVGU0EmsQjkGpM2H8y/CwGtW1C3el8ywxhHKWxgOlaPNj0VcRRW+OoiKvCXF0o6YeXWLQDaNQyMf1Clhsi22D9HUNXOBCVZamaBmiO5BxRdRQOt3M3oFUAD4/HDolSChx7AvXzRIJQtgsUfMu6HB+HglNLc5d5KiwpcAqTH7Idk/lvLD9Z0rUx4vYWL2UJ4WY6XbdL91ML57+EjsRNEMnw/LCrKklN9NNkbuLvKsdabjM/ZMByh+PDWuuw6kDEYXPzeSfzGARlNG1M1ENRCfGLlUuJ5MVTg+UyxGzC+1+KN/DkDyuTSVbqo7vNnagfKPTrH9b8pQtgQ/PRCifDTaUJaIWw8adUycklLrcppkyCZfkJ5cYlSZnQTkmsYf58OYAlMpg6JnlhYlC9uxhIdWvbr1NS8Ahc9pgQlkkai3fOorVUK4JGeYTJIgVTm+mnCqrmSfOgDJ0mOlOlhcmClk3M0KmPzeF0mnDGVB6LjqbmKB8p5GRQ34DStRCdpEpp5MRNWRNocwsjk9i7nyqugzPYTWUSZuqe0qVucAT5tgH9ITmxEdCdihjpcCVAgfI8uJ4pgx3K3UhgBeRQ9dtbJmjp1TnYmsKoSH1UGqKE23mxlrsri4yKsuAFnZ5BrAugypw0/IdSvHmxHJbEI6lREzj0asuOc7TR8BONdd9pNKCo4LRNY9CdgCEXjqObDhQvsFpy7z7DsqHP9khxp9DzNeKbSR+Iy3/n31tqVFYe17xFUZkTu507+4px4USFwBRm32lbzFyXphgRMtn3cwqqaef8a0UrMHlaJYM8RC1Iq2DeOXvKUdVjALmzromST8+4N+Egm9rrwzl/DpAVlddnE9su36Jyx6ECtkUxufaUMJOzfwQsxldUbnTLyO/ckCcNsS112yDmkkGF/4xKL8rHndrowChbKMrV61QgFBWiMepbRQglG105aoVChDKCvE4tY0ChLKNrly1QgFCWSEep7ZRgFC20ZWrVihAKCvE49Q2ChDKNrpy1QoF/gDXIhmWmc+CSAAAAABJRU5ErkJggg=="
    #     imgdata = base64.b64decode(f.read())
    #     file = open('1.jpg', 'wb')
    #     file.write(imgdata)
    #     file.close()


class MyOrderList(generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        sell_id = self.request.query_params.get('sellID', None)
        obj = Order.objects.get(sell_id=sell_id)


class CheckMobile(generics.RetrieveAPIView):
    """确认手机号"""
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def get_object(self):
        pre_mobile = self.request.query_params.get('mobile', None)
        try:
            user = User.objects.get(mobile=pre_mobile)
            return user
        except:
            return None
