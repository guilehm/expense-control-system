web: gunicorn controller.wsgi --log-file -
celery: celery worker -A controller -l info
