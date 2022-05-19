import json
import os
from datetime import datetime

from celery import Celery, shared_task
from celery.utils.log import get_task_logger
# 1-s terminal celery -A MainWater beat
# 2-s terminal celery -A MainWater worker
import requests

from .models import *





@shared_task(name='get_data')
def get_data():
    today = datetime.today().day
    this_month = datetime.today().month
    profiles = Profile.objects.all()
    for profile in profiles:
        if profile.api_key != '':
            user = profile.user
            his_day = profile.day_of_metersdata
            if str(today) == str(his_day):
                his_counters = Counter.objects.filter(user_id=user, isclever=True)
                for counter in his_counters:
                    get_last_data = MetersData.objects.filter(user_id=user, id_counter=counter).latest('id')
                    if int(this_month) != int(str(get_last_data.date)[5:7]):
                        api_body_request = "https://lk.waviot.ru/api.data/get_values/?modem_id=" + counter.id_modem
                        api_key = "&key=" + profile.api_key
                        main_request = requests.get(api_body_request + api_key)
                        last_value = int(
                            json.loads(main_request.text)["registrators"][str(counter.id_registrator)]["values"][-1][
                                "value"])
                        new_meter_data = MetersData.objects.create(user_id=user, id_counter=counter, date=datetime.now(), value=last_value)
                        print(new_meter_data)
                    else:
                        print("not in this month")