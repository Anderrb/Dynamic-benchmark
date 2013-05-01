#!/bin/sh

# User settings
umask 0002
ulimit -c unlimited
ulimit -s unlimited
#ulimit -a
#ulimit -m 8000000
ulimit -v 80000000

# Modules
. /etc/profile.d/modules.sh

module use --append /site/VERSIONS/modulefiles
module purge
module load gcc/4.5.1
module load R/2.13.2.shlib
#module load R/2.15.1.shlib
module load python/2.7.gcc45
#module load python2/2.7.3
module load imagemagick/6.7.2.5
#module load imagemagick/6.7.9-0
#module load perl/1.7
module load perlmodules
module load fastx
module load gnuplot
module load bowtie

# Python
export PYTHONPATH=$HB_SOURCE_CODE_BASE_DIR:$HB_PYTHONPATH

# R
export RHOME=$HB_RHOME
export R_LIBS=$HB_R_LIBS_DIR:$HB_R_LIBS

#For installing R package XML
export XML_CONFIG=/usr/bin/xml2-config
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/local/lib
unset LIBXML_LIBDIR
unset LIBXML_INCDIR

# Xvfb
export DISPLAY=$HB_XVFB_DISPLAY

# Tmp dir
export TMPDIR=$GALAXY_NEW_FILE_PATH
export TMP=$TMPDIR
export TEMP=$TMPDIR
export PYTHON_EGG_CACHE="$TMP/.python-eggs"

# ImageMagick
export MAGICK_MEMORY_LIMIT='30GiB'
export MAGICK_TMPDIR=$TMPDIR

# Galaxy
cd `dirname $0`

python ./scripts/check_python.py
[ $? -ne 0 ] && exit 1

SAMPLES="
    datatypes_conf.xml.sample
    external_service_types_conf.xml.sample
    reports_wsgi.ini.sample
    shed_tool_conf.xml.sample
    tool_conf.xml.sample
    tool_data_table_conf.xml.sample
    tool_sheds_conf.xml.sample
    universe_wsgi.ini.sample
    tool-data/shared/ucsc/builds.txt.sample
    tool-data/shared/igv/igv_build_sites.txt.sample
    tool-data/*.sample
    static/welcome.html.sample
"

# Create any missing config/location files
for sample in $SAMPLES; do
    file=`echo $sample | sed -e 's/\.sample$//'`
    if [ ! -f "$file" -a -f "$sample" ]; then
        echo "Initializing $file from `basename $sample`"
        cp $sample $file
    fi
done

# explicitly attempt to fetch eggs before running. Also start and stop Xfvb as appropriate
FETCH_EGGS=1
START=0
STOP=0
for arg in "$@"; do
    [[ "$arg" = "--stop-daemon" || "$arg" = "stop" ]] && FETCH_EGGS=0 && STOP=1
    [[ "$arg" = "--daemon" || "$arg" = "start" ]] && START=1
done
if [ $FETCH_EGGS -eq 1 ]; then
    python ./scripts/check_eggs.py -q
    if [ $? -ne 0 ]; then
        echo "Some eggs are out of date, attempting to fetch..."
#        python ./scripts/fetch_eggs.py
        python ./scripts/scramble.py -c universe_wsgi.runner.ini
        python ./scripts/hb_scramble.py -c universe_wsgi.runner.ini
        if [ $? -eq 0 ]; then
            echo "Fetch successful."
        else
            echo "Fetch failed."
            exit 1
        fi
    fi
fi

if [ $START -eq 1 ]; then
    echo 'Starting Xvfb on display $HB_XVFB_DISPLAY'
    Xvfb $HB_XVFB_DISPLAY -screen 0 1600x1200x24 -nolisten tcp >$LOG_PATH/xvfb.log 2>&1 &
    echo 'Starting taskqueuemanager...'
	python $HB_SOURCE_CODE_BASE_DIR/quick/application/parallel/TaskQueueReferentManager.py &

elif [ $STOP -eq 1 ]; then
    echo 'Stopping Xvfb on display $HB_XVFB_DISPLAY'
    pkill -f "Xvfb $HB_XVFB_DISPLAY"
    if [ -e taskQueue.pid ]; then
    	PID=`cat taskQueue.pid`
    	echo 'Stopping taskqueuemanager with pid' $PID
        ps -o pid= --ppid $PID | xargs kill
    	kill $PID
    	rm taskQueue.pid
    fi
fi

for i in {0..$GALAXY_ADDITIONAL_WEB_SERVER_COUNT}; do
    python ./scripts/paster.py serve universe_wsgi.webapp.ini --server-name=web$i --pid-file=paster$i.pid --log-file=paster$i.log $@
done
python ./scripts/paster.py serve universe_wsgi.runner.ini --server-name=runner --pid-file=runner.pid --log-file=runner.log $@
