from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import datetime

class Store(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField(default=datetime.datetime.now)
    class Meta:
        db_table = "stores"

class Products(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    display_image = models.ImageField(null=True, upload_to=settings.DISPLAY_IMAGES_FOLDER)
    oss_url = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=datetime.datetime.now)
    updated_date = models.DateTimeField(default=datetime.datetime.now)
    class Meta:
        db_table = "products"
