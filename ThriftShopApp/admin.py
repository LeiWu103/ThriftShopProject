from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(User)
admin.site.register(Goods)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Profile)
admin.site.register(Address)