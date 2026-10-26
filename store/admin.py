from django.contrib import admin
from .models import Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  

class ProductAdmin(admin.ModelAdmin):
    list_display = ('watchname', 'watchbrand', 'watchprice', 'stock_quantity')  
    inlines = [ProductImageInline]  

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
