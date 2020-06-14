from django.contrib import admin

# Register your models here.
from .models import *
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'mobile', 'add_time')
    list_display = ('id','username','mobile')

    ordering = ('-add_time',)
    list_display_links = ('id','username')
admin.site.register(Goods)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Profile)
admin.site.register(Address)