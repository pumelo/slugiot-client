#!usr/bin/env bash
### BEGIN INIT INFO
# Provides:          web2py
# Required-Start:    $local_fs ram_fs
# Required-Stop:
# Default-Start:     S
# Default-Stop:         0 6
# Short-Description: Starts local web2py server, with scheduler running in background for APP.
### END INIT INFO

PATH="/sbin:/bin:/usr/bin"
PID_FILE=/var/run/web2py.pid
USER=pi
APPDIR=/home/pi/Documents
CMD=$APPDIR/slugiot-client/web2py.py
PYTHON=/usr/bin/python
PORT=8080
PASS=password
APP=client

. /lib/lsb/init-functions

do_start () {
    /sbin/start-stop-daemon --start --chuid $USER -d $APPDIR --background -v \
        --user $USER --pidfile $PID_FILE --make-pidfile --exec $PYTHON \
        --startas $PYTHON -- $CMD -a $PASS -p $PORT -K $APP -i 0.0.0.0 -X
    log_success_msg "Started web2py"
    log_failure_msg "Failed to start web2py"
}

do_stop () {
    /sbin/start-stop-daemon --stop -d $APPDIR -v --user $USER --pidfile $PID_FILE \
        --exec $PYTHON --retry 10
    rm $PID_FILE
    log_success_msg "Stopped web2py"
    log_failure_msg "Failed to stop web2py"
}

do_startup(){
    # Fetch internal network ip into variable
    pyip=
    while IFS=$': \t' read -a line ;do
        [ -z "${line%inet}" ] && ip=${line[${#line[1]}>4?1:2]} &&
            [ "${ip#127.0.0.1}" ] && pyip=$ip
      done< <(LANG=C /sbin/ifconfig)

    # Check if webserver up and running and, if so, open web browser to client and
    # run startup script from localhost.
    nc -z $pyip $PORT; wup=$?;
    if [$wup -ne 0]; then
      echo "Connection to $pyip on port $PORT failed"
      exit 1
    else
      echo "Connection to client succeeded; access using http://$pyip:$PORT/"
      echo "Begin call to _start() from localhost..."
      httpUrl="http://127.0.0.1:$PORT/startup/_start.html"
      rep=$(curl -o /dev/null --silent --head --write-out '%{http_code}\n' $httpUrl)
      status=$?
      echo "$rep"
      exit $status
    fi

    log_success_msg "Started $APP"
    log_failure_msg "Failed to start $APP"
}


case "$1" in
  start)
        do_start
        sleep 5
        do_startup
        ;;
  restart|reload|force-reload)
        do_stop || log_failure_msg "Not running"
        do_start
        sleep 5
        do_startup
        ;;
  stop|status)
        do_stop
        ;;
  *)
        echo "Usage: $0 start|stop" >&2
        exit 3
        ;;
esac
