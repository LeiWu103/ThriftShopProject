from rest_framework import serializers
from .models import *
class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model=User
        fields=('id','username')

class VerifyCodeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model=VerifyCode
        fields='__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model=Category
        fields=('id','name',)

class GoodsSerializer(serializers.ModelSerializer):
    category=CategorySerializer()
    seller=UserSerializer()
    class Meta:
        model=Goods
        #fields=('id','name','category','price','image','seller')
        fields=('__all__')

class GoodsDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    seller = UserSerializer()
    class Meta:
        model=Goods
        fields=('__all__')

class OrderSerializer(serializers.ModelSerializer):
    buyer=UserSerializer
    seller=UserSerializer()
    class Meta:
        model=Goods
        fields=('__all__')




class UserCreateSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model=User
        fields=('id','username','password','mobile')
        extra_kwargs={'password':{'write_only':True}}
        def create(self,validated_data):
            user=User(**validated_data)
            return user


class AddressSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Address
        fields=('user','signer','location','mobile')

class ProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer
    class Meta:
        model=Profile
        fields=('__all__')


class OrderCreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ('buyer','goods','message')
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = User(**validated_data)
            return user
