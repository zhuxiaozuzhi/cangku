from django.db import models


class Users(models.Model):
    uid = models.IntegerField()
    email = models.CharField(max_length=30)
    name = models.CharField(max_length=20)
    tel = models.CharField(max_length=11)
    pwd = models.CharField(max_length=100)




