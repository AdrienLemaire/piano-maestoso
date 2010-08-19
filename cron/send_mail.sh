#!/bin/bash

# This script works only in linux
# You should put your virtualenv in ~/Envs
WORKON_HOME=$(readlink -f ~/Envs)
PROJECT_ROOT=$(readlink -f ..)

# activate virtual environment
. $WORKON_HOME/pinax-env/bin/activate

python manage.py send_mail >> $PROJECT_ROOT/logs/cron_mail.log 2>&1
