PATH=/projects/rrresearch/common_software/bin:/usr/sbin:$PATH

GALAXY_ADDITIONAL_WEB_SERVER_COUNT=${GALAXY_ADDITIONAL_WEB_SERVER_COUNT=1}

if [ `id -un` != "ghbrowse" ]; then
  exec sudo -u ghbrowse $0 $1
fi


if [ ! -d "$GALAXY_DIR" ]; then
    echo "$GALAXY_DIR does not exist"
    exit 2
fi

#start_Xvfb () {
#    Xvfb $XVFB_DISPLAY -screen 0 1600x1200x24 -nolisten tcp >$GALAXY_DIR/xvfb.log 2>&1 &
#}
#
#stop_Xvfb () {
#    pkill -f "Xvfb $XVFB_DISPLAY"
#}

start() {
#    start_Xvfb
    sh $GALAXY_DIR/run.sh --daemon 2>/dev/null
}

stop() {
    sh $GALAXY_DIR/run.sh --stop-daemon
    #stop_Xvfb
    rm -f $GALAXY_DIR/*.pid
}

restart() {
    stop
    sleep 5
    start
}


DOUBLECHECK=0

check() {
    RETVAL=0
    PIDS=`ls $GALAXY_DIR/*.pid 2>/dev/null`
#    echo $PIDS
    CRASHED=0
    if [ "$PIDS" != "" ]; then
      NUM_PIDS=-1
      for p in $PIDS; do
	    (( NUM_PIDS++ ))
	    kill -0 `cat $p` || CRASHED=1
      done
	  if [ $NUM_PIDS -lt "$GALAXY_ADDITIONAL_WEB_SERVER_COUNT" ]; then
	    CRASHED=1
	    echo "too few pid-files: $NUM_PIDS"
	  fi
    fi
    if [ "$CRASHED" != 0 ]; then
      if [ "$DOUBLECHECK" == 1 ]; then
        echo "processes are dead, restarting..."
        restart
      else
        echo "processes are dead, waiting 30 sec..."        
        DOUBLECHECK=1
        sleep 30
        check
      fi
    fi

    if [ -e "$GALAXY_DIR/NEED_RESTART" ]; then
      echo "NEED_RESTART flagged, restarting..."
      rm -f "$GALAXY_DIR/NEED_RESTART"
      restart
    fi
    
    coredumpsbt
}

coredumps() {
    find "$GALAXY_DIR/" -name 'core.*' -mmin -10
}

coredumpsbt() {
    if [ ! -e $GALAXY_DIR/.last_core_dump ]; then
        touch $GALAXY_DIR/.last_core_dump
    fi
    dumps=$(find $GALAXY_DIR/ -maxdepth 1 -name 'core.*' -newer $GALAXY_DIR/.last_core_dump)
    #echo $dumps
    if [ "$dumps" != "" ]; then
        touch $GALAXY_DIR/.last_core_dump
        . /etc/profile.d/modules.sh
        module load python/2.7.gcc45
        for dump in $dumps; do
            echo "# Stacktrace for $dump"
            gdb --quiet --batch -ex bt python $dump 2>/dev/null
	    #rm -f $dump
            echo
        done
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
  coredumps)
	coredumpsbt
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
