from django.db import models
from django.conf import settings
import os

def get_upload_path(instance, filename):
    return os.path.join('images', filename)

class Worker(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    experience = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if self.pk:
            # Get the existing model instance
            old_instance = Worker.objects.get(pk=self.pk)
            # Check if the photo field has changed
            if self.photo and self.photo != old_instance.photo:
                # Delete the old photo from the media directory
                if old_instance.photo:
                    old_instance.photo.delete()
        super().save(*args, **kwargs)

def get_image_list():
    image_directory = os.path.join(settings.MEDIA_ROOT, 'images')
    image_list = []

    for filename in os.listdir(image_directory):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_url = os.path.join(settings.MEDIA_URL, 'images', filename)
            image_list.append(image_url)

    return image_list