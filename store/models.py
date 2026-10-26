from django.db import models
from customer.models import UserDetails
# Create your models here.



class Product(models.Model):
    userid=models.CharField(max_length=12)
    watchimage = models.ImageField()
    watchname = models.CharField(max_length=200)
    watchbrand = models.CharField(max_length=100)
    watchprice = models.DecimalField(max_digits=10, decimal_places=2)
    watchdescription = models.TextField()
    stock_quantity = models.IntegerField()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='additional_images', on_delete=models.CASCADE)
    image = models.ImageField()
