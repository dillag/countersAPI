import os
from datetime import datetime
from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger

# 1-s terminal celery -A MainWater beat
# 2-s terminal celery -A MainWater worker --loglevel=info


logger = get_task_logger(__name__)
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MainWater.settings')

app = Celery('MainWater', broker="redis://localhost:7777")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.

app.conf.timezone = 'UTC'


#@app.on_after_configure.connect
#def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
#    sender.add_periodic_task(10.0, get_data_from_clever_counters.s('hello'), name='add every 10')


app.conf.beat_schedule = {
    "every day between 6 AM & 18 PM": {
        "task": "get_data",  # <---- Name of task
        "schedule": 60.0
    },
}

app.autodiscover_tasks()

@app.task
def test(arg):
    print(arg)


@app.task
def get_data_from_clever_counters(args, **kwargs):
    today = datetime.today().day
    today1 = datetime.today().month
    print(today, today1)
