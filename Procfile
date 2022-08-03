web: python manage.py runserver 0.0.0.0:\$PORT
# web: gunicorn website_change_detector.wsgi --log-file - --log-level debug
worker: celery -A website_change_detector worker -loglevel info 
beat: celery -A website_change_detector beat -loglevel info