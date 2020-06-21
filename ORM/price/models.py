from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Product(models.Model):
    name = models.CharField('이름', max_length=150, unique=True)
    price = models.IntegerField('가격')

class OrderLog(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    created = models.DateTimeField('판매일', default=timezone.now())

@receiver(post_save, sender=Product)
def save_orderlog(sender, instance, **kwargs):
    OrderLog.objects.create(product=instance)
