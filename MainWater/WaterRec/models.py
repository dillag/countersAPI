from django.db import models
from django.contrib.auth.models import User
from .choices import EventStatus
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    fullname = models.CharField(max_length=60, blank=True)
    place = models.CharField(max_length=60, blank=True)
    number_phone = models.CharField(max_length=11, blank=True)
    default_password = models.BooleanField(default=True)
    api_key = models.CharField(max_length=50, default=None)
    day_of_metersdata = models.CharField(max_length=2, default=1)

    def __str__(self):
        return self.user.__getattribute__('username')


class Service_Record(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.CharField(max_length=300, choices=EventStatus.choices)
    description = models.CharField(max_length=300)
    DateTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)


class Counter(models.Model):
    id_counter = models.IntegerField()
    typewater = models.IntegerField(default=0)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    isclever = models.BooleanField(default=False)
    id_modem = models.CharField(default="", max_length=15)
    id_registrator = models.CharField(default="", max_length=30)

    def __str__(self):
        return str(self.id)


class MetersData(models.Model):
    id_counter = models.ForeignKey(Counter, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    year = models.CharField(default="2022", max_length=4)
    value = models.CharField(default="00000", max_length=6)
    water_flow = models.IntegerField(default=0)

    def __str__(self):
        return str(self.value)
