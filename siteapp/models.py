from django.db import models

# Create your models here.

class File(models.Model):
    id = models.AutoField(primary_key=True)
    filetype = models.CharField(max_length=10)
    md5 = models.TextField()

    def __str__(self):
        return self.md5

class Counts(models.Model):
    id = models.AutoField(primary_key = True)
    date = models.TextField()
    visitors = models.IntegerField()
    conversions = models.IntegerField()

    def __str__(self):
        return self.date