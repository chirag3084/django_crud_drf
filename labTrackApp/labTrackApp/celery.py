import os
from celery import Celery

# default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'labTrackApp.settings')

# create the Celery application instance
# string 'labTrackApp' is the name of the Celery app
app = Celery('labTrackApp', 
             broker='redis://localhost:6379/0',
            )

# load configuration from Django settings file (settings.py)
app.config_from_object('django.conf:settings', namespace='CELERY')

# auto-discover task modules in all installed Django apps
# looks for a tasks.py file in each app (e.g., instruments/tasks.py)
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')