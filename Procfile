web: newrelic-admin run-program gunicorn controller.wsgi --log-file -
celery: celery worker -A controller -l info
