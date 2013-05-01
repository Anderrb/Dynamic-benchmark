#!/bin/bash

if [ `id -un` != "ghbrowse" ]; then
  exec sudo -u ghbrowse $0
fi

umask 0002

#RSYNC="/local/bin/rsync -rtpuOK --stats --delete-during --max-delete=200000 --bwlimit=50000" 
RSYNC="/local/bin/rsync -rtpuOK --stats --delete-before --inplace --ignore-errors --bwlimit=50000" 

/usr/bin/pgrep -f "$RSYNC"
running=$?

if [ $running == 0 ]; then
  echo "rsync is still running"
  exit
fi

nice -n 15 $RSYNC /usit/invitro/hyperbrowser/ /norstore_osl/hyperbrowser/sync/ >/tmp/sync_to_norstore.log 2>&1
