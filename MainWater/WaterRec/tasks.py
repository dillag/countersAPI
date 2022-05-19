from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Counter, Profile, MetersData
from datetime import datetime


@shared_task(name="get_data_from_clever_counters")
def get_data_from_clever_counters(name, *args, **kwargs):
    today = datetime.today()
    print(today)

    print("Celery is working!! {} have implemented it correctly.".format(name))