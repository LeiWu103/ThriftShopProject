from django.conf.urls import url

from ThriftShopApp import views

urlpatterns = [
    # 主页路由
    url(r'GoodsDetail/$', views.GoodsDetail.as_view(), name='Goods-detail'),
    url(r'^Category/$', views.CategoryListView.as_view(), name='Category-detail'),
    url(r'^GoodsByCategory/$', views.GoodsListByCategory.as_view(), name='Goods-detail'),
    url(r'^GoodsSelect/$', views.GoodsSelect.as_view(), name='Goods-detail'),
    url(r'^UserCreate/$', views.UserCreateView.as_view(), name='Goods-detail'),
    url(r'^AddressList/$', views.AddressListView.as_view(), name='Address-detail'),
    url(r'^ProfileRUView/$', views.ProfileRUView.as_view(), name='Profile-detail'),
    url(r'^LoginInfo/$', views.LoginView.as_view(), name='Login-detail'),
    url(r'^OrderCreate/$', views.OrderCreatView.as_view(), name='Order-detail'),
    url(r'^CheckMobile/$', views.CheckMobile.as_view(), name='Order-detail'),
    # 个人中心路由
    url(r'^MySellGoods/$', views.MySellGoodsList.as_view(), name='Goods-detail'),
    url(r'^MyBuyGoods/$',views.MyBuyGoodsList.as_view(),name='Goods-detail'),
    url(r'^ChangePassword/$', views.ChangePassword.as_view(), name='User-detail'),
    url(r'^AddressCreate/$', views.AddressCreate.as_view(), name='Address-detail'),
    url(r'^AddressRUD/(?P<pk>[0-9]+)/$', views.AddressRUD.as_view(), name='Address-detail'),
    url(r'^GoodsCreate/$', views.GoodsCreate.as_view(), name='Goods-detail'),
    url(r'^OrderList/$', views.OrderList.as_view(), name='Order-detail'),
    url(r'^OrderDetail/$', views.OrderDetail.as_view(), name='Order-detail'),
    url(r'^OrderRUD/(?P<pk>[0-9]+)/$', views.OrderRUD.as_view(), name='Order-detail'),
    url(r'^ImageUpload/$', views.ImageUpload.as_view(), name='Image-detail'),
    url(r'^GoodsRUD/(?P<pk>[0-9]+)/$', views.GoodsRUD.as_view(), name='Goods-detail'),
    url(r'^ProfileEdit/$', views.ProfileEdit.as_view(), name='profile-detail'),
]
