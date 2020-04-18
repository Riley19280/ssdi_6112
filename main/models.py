from django.db import models
from accounts.models import User
# Create your models here.


class facebook_data_upload(models.Model):
    dataset_name = models.CharField(max_length=32)
    file_name = models.CharField(max_length=64)
    upload_file_name = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
