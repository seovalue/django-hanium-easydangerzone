# -*- coding: utf-8 -*-
from django.db import models

# Create your models here
def get_file_path(instance, filename):
    return '/upload_file'

upload_files = models.FileField(upload_to=get_file_path, null=True, blank=True, verbose_name='파일')
filename = models.CharField(max_length=64, null=True, verbose_name='첨부파일명')