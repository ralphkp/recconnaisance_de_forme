# celeryconfig.py
broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'


#celery -A app.celery worker --loglevel=info
