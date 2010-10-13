#!/bin/bash

# This script works only in linux
WORKON_HOME=$(readlink -f /home/adrien/Envs)
PROJECT_ROOT=$(readlink -f /var/lib/django/piano-maestoso)

# activate virtual environment
. $WORKON_HOME/piano-maestoso/bin/activate

python $PROJECT_ROOT/manage.py retry_deferred >> $PROJECT_ROOT/logs/cron_mail.log 2>&1
