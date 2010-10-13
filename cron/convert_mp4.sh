#!/bin/bash

# This script works only in linux
WORKON_HOME=$(readlink -f /home/adrien/Envs)
PROJECT_ROOT=$(readlink -f /var/lib/django/piano-maestoso)

echo "cron mp4 executed" >> $PROJECT_ROOT/logs/cron_hello.log

# activate virtual environment
source $WORKON_HOME/piano-maestoso/bin/activate

python $PROJECT_ROOT/manage.py convert_videos mp4 >> $PROJECT_ROOT/logs/cron_video.log 2>&1
