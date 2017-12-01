from django.db import models

class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    uemail = models.CharField(max_length=30)
    uaddressee = models.CharField(max_length=20,default='')
    uaddress = models.CharField(max_length=100,default='')
    upostal_code = models.CharField(max_length=6,default='')
    uphone = models.CharField(max_length=11,default='')


# Create your models here.
