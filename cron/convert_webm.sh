#!/bin/bash

# This script works only in linux
WORKON_HOME=$(readlink -f /home/adrien/Envs)
PROJECT_ROOT=$(readlink -f /var/lib/django/piano-maestoso)

echo "cron webm executed" >> $PROJECT_ROOT/logs/cron_hello.log

# activate virtual environment
. $WORKON_HOME/piano-maestoso/bin/activate

python -c "import os; os.environ['PATH'] += ':/usr/local/bin/'; print os.environ['PATH']" >> $PROJECT_ROOT/logs/cron_video.log 2>&1
python $PROJECT_ROOT/manage.py convert_videos webm >> $PROJECT_ROOT/logs/cron_video.log 2>&1
