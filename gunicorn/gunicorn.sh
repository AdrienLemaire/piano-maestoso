#!/bin/sh

### BEGIN INIT INFO
# Provides:       seismic_web
# Required-Start: $local_fs $syslog
# Required-Stop:  $local_fs $syslog
# Default-Start:  2 3 4 5
# Default-Stop:   0 1 6
# Short-Description: Gunicorn processes for seismic_web
### END INIT INFO

# www-data is the default www user on debian
USER=adrien
NAME="piano_maestoso"
PYTHON_PATH="/home/adrien/Envs/piano-maestoso/bin/python"
MANAGE_PATH="/home/adrien/piano-maestoso/manage.py"
GUNICORN_CONFIG_PATH="/home/adrien/piano-maestoso/gunicorn_conf.py"
# Confdir: the Django project inside the virtualenv
CONFDIR="/home/adrien/piano-maestoso/"
#VENV_ACTIVATION=". ../bin/activate"
RETVAL=0
# PID: I always name my gunicorn pidfiles this way
PID="/tmp/gunicorn_"$NAME".pid"
#COMMAND="$GUNICORN_RUN --daemon --pid $PID"
GUNICORN_RUN="$PYTHON_PATH $MANAGE_PATH run_gunicorn --daemon --pid $PID -c $GUNICORN_CONFIG_PATH"

# source function library
. /lib/lsb/init-functions


start()
{
    echo "Starting $NAME."
    cd $CONFDIR;
    su -c "$GUNICORN_RUN" $USER && echo "OK" || echo "failed";
}

stop()
{
    echo "Stopping $NAME"
    kill -QUIT `cat $PID` && echo "OK" || echo "failed";
}

reload()
{
    echo "Reloading $NAME:"
    if [ -f $PID ]
    then kill -HUP `cat $PID` && echo "OK" || echo "failed";
    fi
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        reload
        ;;
    reload)
        reload
        ;;
    force-reload)
        stop && start
        ;;
    *)
        echo $"Usage: $0 {start|stop|restart}"
        RETVAL=1
esac
exit $RETVAL
