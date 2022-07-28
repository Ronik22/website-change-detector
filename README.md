# website-change-detector
- Detects website changes (full/part of) using image / html / text comparisons and emails the user a file with the changes highlighted. 

- User can set a threshold value (default = 1.0). 

- For tracking a part of webpage use XPath of the element.

## Adding env variables

- Add env variables to ".env.test" and rename it to ".env"

## Installation

```bash
$ python -m venv venv
$ source venv/Scripts/activate
(venv) pip install -r requirements.txt
(venv) cd website-change-detector
(venv) python manage.py makemigrations
(venv) python manage.py migrate
(venv) python manage.py createsuperuser
(venv) python manage.py runserver
```

## Celery run command

Run both commands on separate terminals

```bash
celery -A website_change_detector.celery worker --pool=solo -l info
celery -A website_change_detector beat -l info
```

If you want to run in background
```bash
celery -A website_change_detector.celery worker --pool=solo -l info --logfile=celery.log --detach
celery -A website_change_detector beat -l info --logfile=celery.beat.log --detach 
```

## Test Coverage

```bash
coverage run manage.py test && coverage report && coverage html
```

## Running Tests

To run tests, run the following command

```bash
python manage.py test
```

## Deploy to Heroku

https://devcenter.heroku.com/articles/getting-started-with-python

https://realpython.com/django-hosting-on-heroku/