#!/bin/bash


python manage.py migrate
python manage.py runserver 0.0.0.0:80
# Need this here to keep the docker container running
/bin/bash
tail -f /dev/null