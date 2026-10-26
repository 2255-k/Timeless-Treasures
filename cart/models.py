from django.db import models
from customer . models import UserDetails
from store . models import Product

class CartZ(models.Model):
    cuser = models.IntegerField()  
    cartimage = models.ImageField(upload_to='cart_images/', null=True, blank=True)  
    cartname = models.CharField(max_length=200)
    cartbrand = models.CharField(max_length=100)
    cartprice = models.FloatField()  
    cartdescription = models.TextField()
    quantity = models.IntegerField(default=1)

class ShippingAddress(models.Model):
    user_details_id = models.IntegerField()  
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

class Payment(models.Model):
    user_id = models.IntegerField() 
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('ORDER_PLACED', 'Order Placed'),       
        ('PROCESSING_ORDER', 'Processing Order'), 
        ('QUALITY_CHECK', 'Quality Check'),     
        ('DISPATCHED', 'Dispatched'),           
        ('SHIPPED', 'Shipped'),                 
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),  
        ('DELIVERED', 'Delivered'),             
    ]
    
    user_id = models.IntegerField()  
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.IntegerField()  
    status = models.CharField(max_length=20,choices=ORDER_STATUS_CHOICES, default='ORDER_PLACED' )

class OrderItem(models.Model):
    order_id = models.IntegerField()  
    product_name = models.CharField(max_length=200)
    product_brand = models.CharField(max_length=100)
    product_price = models.FloatField()
    product_quantity = models.IntegerField(default=1)
    total_amount = models.FloatField()

