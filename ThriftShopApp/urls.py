from django.conf.urls import url

from ThriftShopApp import views

urlpatterns=[
    url(r'GoodsDetail/$',views.GoodsDetail.as_view(),name='Goods-detail'),
    url(r'^Category/$',views.CategoryListView.as_view(),name='Category-detail'),
    url(r'^GoodsByCategory/$',views.GoodsListByCategory.as_view(),name='Goods-detail'),
    url(r'^GoodsSelect/$',views.GoodsSelect.as_view(),name='Goods-detail'),
    url(r'^UserCreate/$',views.UserCreateView.as_view(),name='Goods-detail')
]