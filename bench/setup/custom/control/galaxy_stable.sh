#!/bin/sh

GALAXY_NAME="galaxy_stable"
GALAXY_DIR="/usit/invitro/data/galaxy/$GALAXY_NAME"
XVFB_DISPLAY=":10"
GALAXY_ADDITIONAL_WEB_SERVER_COUNT=3

. `dirname $0`/control.sh
