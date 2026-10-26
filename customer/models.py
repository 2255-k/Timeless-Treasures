from django.db import models


# Create your models hee.

class UserDetails(models.Model):
    username = models.CharField(max_length=200)
    userphone = models.CharField(max_length=200)
    useremail = models.CharField(max_length=12)
    userpassword = models.CharField(max_length=200)


class bankdetailz(models.Model):
    bankuser = models.IntegerField() 
    holdername = models.CharField(max_length=200)
    accountno = models.CharField(max_length=200)
    ifsc = models.CharField(max_length=200)


class Notification(models.Model):
    notid = models.IntegerField() 
    message = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
