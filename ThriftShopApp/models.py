from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    username=models.CharField('用户名',max_length=30)
    password=models.CharField('用户密码',max_length=50)
    mobile=models.CharField('手机号',max_length=16)
    add_time=models.DateTimeField('添加时间',default=timezone.now())
    class Meta:
        db_table='User'

class VerifyCode(models.Model):
    code=models.CharField('验证码',max_length=50,null=False)
    mobile=models.CharField('手机号',max_length=16,null=False)
    add_time = models.DateTimeField('添加时间',default=timezone.now())
    class Meta:
        db_table = 'VerifyCode'

class Category(models.Model):
    name=models.CharField('类别名',max_length=30)
    add_time=models.DateTimeField('添加时间',default=timezone.now())

    class Meta:
        db_table='Category'

class Goods(models.Model):
    category=models.ForeignKey('Category',on_delete=models.CASCADE)
    seller=models.ForeignKey('User',on_delete=models.CASCADE)
    name=models.CharField('商品名',max_length=30)
    amount=models.IntegerField('商品数量')
    click=models.IntegerField('点击量',default=0)
    price=models.FloatField('单价')
    brief=models.CharField('简介',max_length=1000)
    image=models.CharField('商品图片',max_length=300)
    transaction=models.SmallIntegerField('交易方式')
    payment=models.BooleanField('交易方式',default=True)
    postage=models.FloatField('运费')
    add_time=models.DateTimeField('加入时间',default=timezone.now())
    class Meta:
        db_table='Goods'

class Order(models.Model):
    buyer=models.ForeignKey('User',on_delete=models.CASCADE,related_name='buyer')
    goods=models.ForeignKey('Goods',on_delete=models.CASCADE)
    order_sn=models.IntegerField('订单号',unique=True,null=False)
    status=models.CharField('订单状态',max_length=10)
    cost=models.FloatField('订单金额')
    message=models.CharField('订单留言',max_length=200)
    contact = models.CharField('联系方式', max_length=30)
    add_time=models.DateTimeField('添加时间',default=timezone.now())
    class Meta:
        db_table='Order'

class Address(models.Model):
    user=models.ForeignKey('User',on_delete=models.CASCADE)
    signer=models.CharField('收件人',max_length=20)
    location=models.CharField('位置',max_length=500)
    mobile=models.CharField('手机号',max_length=16)
    # contact = models.CharField('联系方式', max_length=30)
    add_time=models.DateTimeField('添加时间',default=timezone.now())
    class Meta:
        db_table='Address'

class Profile(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    bio=models.CharField('签名',max_length=1000)
    email=models.EmailField('邮箱')
    add_time = models.DateTimeField('添加时间', default=timezone.now())
    class Meta:
        db_table = 'Profile'

