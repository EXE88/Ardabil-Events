from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
import uuid
import os

def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4()}.{ext}"
    return f"images/{new_filename}"

class CreatePost(models.Model):
    class Subject(models.TextChoices):
        NAZRI = 'N', 'نذری'
        DAVA = 'D', 'دعوا'

    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False)
    subject_choise = models.CharField(max_length=1,choices=Subject.choices)
    image = models.ImageField(upload_to=upload_to,null=False,blank=False)
    title = models.CharField(max_length=60,null=False,blank=False)
    description = models.TextField(max_length=200,blank=True, null=False)
    latitude = models.FloatField(null=False,blank=False)
    longitude = models.FloatField(null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

@receiver(post_delete, sender=CreatePost)
def delete_image_file(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)