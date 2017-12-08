# coding=utf8
from django.db import models
from tinymce.models import HTMLField

class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.ttitle.encode('utf8')

class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20,default='梨子号')
    gpic = models.ImageField(upload_to='df_goods')
    gprice = models.DecimalField(max_digits=5,decimal_places=2,default=10)
    isDelete = models.BooleanField(default=False)
    gunit=models.CharField(max_length=10,default='500g')
    gclick=models.IntegerField(default=21)
    gprofile=models.CharField(max_length=200,default='简介')
    gstock=models.IntegerField(default=50)
    gcontent=HTMLField(default='内容')
    gtype=models.ForeignKey(TypeInfo)
    def __str__(self):
        return self.gtitle.encode('utf8')

