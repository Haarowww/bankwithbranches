from django.db import models
from django.contrib.auth.models import User
from django.db.models import CASCADE


# Create your models here.
class Branch(models.Model):
    name = models.CharField(max_length=200)
    transit_num = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    email = models.EmailField(default="admin@utoronto.ca")
    capacity = models.PositiveIntegerField(null=True)
    last_modified = models.DateTimeField(auto_now=False)
    id = models.AutoField(primary_key=True)


class Bank(models.Model):
    name = models.CharField(max_length=200)
    swift_code = models.CharField(max_length=200)
    inst_num = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    owner = models.ForeignKey(to=User, on_delete=CASCADE, related_name="bank_owner", null=True)
    id = models.AutoField(primary_key=True)
    branches = models.ManyToManyField(Branch)
