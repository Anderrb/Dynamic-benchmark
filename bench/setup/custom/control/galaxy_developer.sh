#!/bin/sh

GALAXY_NAME="galaxy_developer"
GALAXY_DIR="/usit/invitro/data/galaxy/$GALAXY_NAME"
XVFB_DISPLAY=":9"
GALAXY_ADDITIONAL_WEB_SERVER_COUNT=1

. `dirname $0`/control.sh