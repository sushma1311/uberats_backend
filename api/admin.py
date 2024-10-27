# admin.py

from django.contrib import admin
from .models import Restaurant, Customer,Dish,Cart,Order, Favorite, Address
# Register your models
admin.site.register(Restaurant)
admin.site.register(Customer)
admin.site.register(Dish)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Favorite)
admin.site.register(Address)


