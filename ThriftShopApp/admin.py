from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'mobile', 'add_time')
    list_display = ('id','username','mobile')
    ordering = ('-add_time',)
    list_display_links = ('id','username')
    search_fields = ('id','username')
@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    raw_id_fields = ("seller","category")
    list_display = ('id', 'name')
    readonly_fields = ('add_time',)
    ordering = ('-add_time',)
    list_display_links = ('id', 'name')
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    readonly_fields = ('add_time',)
    ordering = ('-add_time',)
    list_display_links = ('id', 'name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    raw_id_fields = ("buyer","goods")
    list_display = ('id','order_sn','add_time')
    readonly_fields = ('add_time',)
    ordering = ('-add_time',)
    list_display_links = ('id', 'order_sn','add_time')
