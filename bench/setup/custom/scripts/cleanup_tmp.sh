#!/bin/sh

find /usit/invitro/work/tmp/ -user ghbrowse -name 'Rtmp*' -type d -maxdepth 1 -mtime +7 |xargs rm -rf

