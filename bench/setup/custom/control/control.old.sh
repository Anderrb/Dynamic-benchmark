PATH=/usr/sbin:$PATH

GALAXY_ADDITIONAL_WEB_SERVER_COUNT=${GALAXY_ADDITIONAL_WEB_SERVER_COUNT=1}

if [ `id -un` != "ghbrowse" ]; then
  exec sudo -u ghbrowse $0 $1
fi


if [ ! -d "$GALAXY_DIR" ]; then
    echo "$GALAXY_DIR does not exist"
    exit 2
fi

start_Xvfb () {
    Xvfb $XVFB_DISPLAY -screen 0 1600x1200x24 -nolisten tcp >$GALAXY_DIR/xvfb.log 2>&1 &
}

stop_Xvfb () {
    pkill -f "Xvfb $XVFB_DISPLAY"
}

start() {
    start_Xvfb
    $GALAXY_DIR/run.sh --daemon 2>/dev/null
}

stop() {
    $GALAXY_DIR/run.sh --stop-daemon 2>/dev/null
    stop_Xvfb
    rm -f $GALAXY_DIR/*.pid
}

restart() {
    stop
    sleep 5
    start
}

check() {
    RETVAL=0
    PIDS=`ls $GALAXY_DIR/*.pid 2>/dev/null`
#    echo $PIDS
    if [ "$PIDS" != "" ]; then
      rm -f "$GALAXY_DIR/crashed"
	  NUM_PIDS=-1
      for p in $PIDS; do
	    (( NUM_PIDS++ ))
	    kill -0 `cat $p` || touch "$GALAXY_DIR/crashed"
      done
	  if [ $NUM_PIDS -lt "$GALAXY_ADDITIONAL_WEB_SERVER_COUNT" ]; then
	    touch "$GALAXY_DIR/crashed"
	  fi
	fi
    if [ -e "$GALAXY_DIR/crashed" ]; then
#      echo "processes are dead, restarting..."
      restart
    fi
}

status() {
    PIDS=$(/usr/sbin/lsof -t $GALAXY_DIR/*)
    for pid in $PIDS; do
      ps -flw -p $pid
      lsof -p $pid -a -nPi
      echo
    done
}

cleanup() {
    . /etc/profile.d/modules.sh
    module load python/2.7.gcc45
    cd $GALAXY_DIR/scripts/cleanup_datasets
#    rm *.log
    sh delete_userless_histories.sh
    sh purge_histories.sh
    sh purge_libraries.sh
    sh purge_folders.sh
#    sh delete_datasets.sh
    sh purge_datasets.sh
#    cat *.log
}

case "$1" in
  start)
        start
        ;;
  stop)
        stop
        ;;
  restart)
        restart
        ;;
  check)
	check
	;;
  cleanup)
	cleanup
	;;
  status)
	status
        #RETVAL=$?
        ;;
  *)
        echo $"Usage: $0 {start|stop|restart|status|cleanup}"
        RETVAL=1
esac

exit $RETVAL
