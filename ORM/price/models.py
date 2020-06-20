from django.db import models

class Product(models.Model):
    name = models.CharField('이름', max_length=150, unique=True)
    price = models.IntegerField('가격')

class OrderLog(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    created = models.DateTimeField('판매일', auto_now_add=True)



