#!/bin/bash

# This script works only in linux
WORKON_HOME=$(readlink -f ~/Envs)
PROJECT_ROOT=$(readlink -f ~/piano-maestoso/)

# activate virtual environment
. $WORKON_HOME/piano-maestoso/bin/activate

python $PROJECT_ROOT/manage.py convert_videos webm >> $PROJECT_ROOT/logs/cron_video.log 2>&1
