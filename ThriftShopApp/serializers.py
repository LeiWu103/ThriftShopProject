from rest_framework import serializers
from .models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'account', 'password')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)


class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    seller = UserSerializer()

    class Meta:
        model = Goods
        fields = ('id', 'name', 'category', 'price', 'image', 'seller','amount')


class GoodsDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    seller = UserSerializer()

    class Meta:
        model = Goods
        fields = ('__all__')


class GoodsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ('name','amount','price','brief','transaction','postage','category','seller','code')




class UserCreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'mobile' ,'account')


class ProfileCreateSerializer(serializers.HyperlinkedModelSerializer):
    user = UserCreateSerializer()

    class Meta:
        model = Profile
        fields = ('user',)


class AddressSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Address
        fields = ('id', 'user', 'signer', 'location', 'mobile')


class AddressSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'signer', 'location', 'mobile','user')

class OrderSerializer(serializers.ModelSerializer):
    buyer = UserSerializer()
    goods = GoodsSerializer()
    address=AddressSerializer()
    class Meta:
        model = Order
        fields = ('__all__')

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ('user', 'bio', 'email', )


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'buyer', 'goods', 'address', 'contact', 'message', 'cost', 'status', 'order_sn')
        read_only_fields = ('price', 'cost', 'status', 'order_sn',)


class OrderRUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id',)


class ImageUploadSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Image
        fields = ('id','image',)



