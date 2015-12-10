from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from services import upload_oss_obj, register_oss_object
from dirtyfields import DirtyFieldsMixin
import datetime
import uuid

from django.db.models.signals import post_save
from django.dispatch import receiver


class Store(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    bucket_id = models.CharField(max_length=200, default=str(uuid.uuid4()))
    description = models.CharField(max_length=200, default=None, blank=True)
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = "stores"
    def button(self):
        return mark_safe('<a href="/store/'+str(self.id)+'">View Store</a>')
    button.short_description = ''
    button.allow_tags = True

class Products(DirtyFieldsMixin, models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.FloatField(help_text="Value in $")
    display_image = models.ImageField(null=True, upload_to=settings.DISPLAY_IMAGES_FOLDER)
    oss_url = models.FileField(verbose_name="Geometry File", help_text="Your Geometry file", upload_to=settings.GEOMETRY_FILES)
    oss_object = models.CharField(max_length=200, default=None, blank=True)
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField(default=datetime.datetime.now())
    class Meta:
        db_table = "products"

    def display_img(self):
        return '<img src="%s"/>' % self.display_image
    display_img.allow_tags = True

    def save(self, *args, **kw):
        if self.pk is None:
            self.created_date = datetime.datetime.now()
        super(Products, self).save(*args, **kw)

    def __unicode__(self):
        return str(self.id);

# method for updating
@receiver(post_save, sender=Products)
def update_oss(sender, instance, **kwargs):

    print "Uploading File"
    file_name = instance.oss_url.url.split('/')[-1]
    oss_object_id = upload_oss_obj(instance.store.bucket_id, instance.oss_url.url, file_name)
    print "OSS Object Id %s" % oss_object_id
    print "Upload done"

    if oss_object_id :
        print "Registering File"
        register_oss_object(oss_object_id)
        print "Register done"

    post_save.disconnect(update_oss, sender=Products)
    instance.oss_object = oss_object_id
    instance.save()
    post_save.connect(update_oss, sender=Products)
