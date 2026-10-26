from django.contrib import admin
from. models import CartZ,ShippingAddress,Payment,Order,OrderItem
# Register your models here.

admin.site.register(CartZ)
admin.site.register(ShippingAddress)
admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderItem)
