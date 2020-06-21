from rest_framework import serializers
from .models import *
class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model=User
        fields=('id','username')





class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model=Category
        fields=('id','name',)

class GoodsSerializer(serializers.ModelSerializer):
    category=CategorySerializer()
    seller=UserSerializer()
    class Meta:
        model=Goods
        fields=('id','name','category','price','image','seller')

        #fields=('__all__')

class GoodsDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    seller = UserSerializer()

    class Meta:
        model=Goods
        fields=('__all__')


class OrderSerializer(serializers.ModelSerializer):
    buyer=UserSerializer()
    goods=GoodsSerializer()
    class Meta:
        model=Order
        fields=('__all__')





class UserCreateSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model=User
        fields=('id','username','password','mobile')



class AddressSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Address
        fields=('id','user','signer','location','mobile')

class ProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer
    class Meta:
        model=Profile
        fields=('__all__')


class OrderCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('id','buyer','goods','address','contact','message','cost','status','order_sn')
        read_only_fields=('price','cost','status','order_sn',)


