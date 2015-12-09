from django.db import models
from django.contrib.auth.models import User

class Store(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    class Meta:
        db_table = "stores"

class Products(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    display_image = models.CharField(max_length=200)
    oss_url = models.CharField(max_length=200)
    class Meta:
        db_table = "products"
