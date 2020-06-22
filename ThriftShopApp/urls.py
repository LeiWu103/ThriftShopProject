from django.conf.urls import url

from ThriftShopApp import views

urlpatterns=[
    #主页路由
    url(r'GoodsDetail/$',views.GoodsDetail.as_view(),name='Goods-detail'),
    url(r'^Category/$',views.CategoryListView.as_view(),name='Category-detail'),
    url(r'^GoodsByCategory/$',views.GoodsListByCategory.as_view(),name='Goods-detail'),
    url(r'^GoodsSelect/$',views.GoodsSelect.as_view(),name='Goods-detail'),
    url(r'^UserCreate/$',views.UserCreateView.as_view(),name='Goods-detail'),
    url(r'^AddressList/$',views.AddressListView.as_view(),name='Address-detail'),
    url(r'^ProfileRUView/$',views.ProfileRUView.as_view(),name='Profile-detail'),
    url(r'^LoginInfo/$',views.LoginView.as_view(),name='Login-detail'),
    url(r'^OrderCreate/$',views.OrderCreatView.as_view(),name='Order-detail'),
    #个人中心路由
    url(r'^MySellGoods/$',views.MySellGoodsList.as_view(),name='Goods-detail'),
    url(r'^MyBuyGoods/$',views.MyBuyGoodsList.as_view(),name='Goods-detail'),
]