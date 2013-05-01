if [ $# -ne 2 ]
then
    echo "usage:   release.sh from_prefix to_prefix"
    echo "example: release.sh rc stable"
    exit
fi

from="$1"
to="$2"

function checkIfDir {
    if [ ! -d $1 ]
    then
	echo "'$1' is not an existing directory"
	exit
    fi
}

galaxyDir='/usit/invitro/data/galaxy'
hbDir='/usit/invitro/data/hyperbrowser'
dbDumpDir='/usit/invitro/data/galaxy/db_dumps'

checkIfDir $galaxyDir
checkIfDir $hbDir
checkIfDir $dbDumpDir

fromTempFn="/tmp/$RANDOM.col1"
toTempFn="/tmp/$RANDOM.col1"

function findCorrectDirs {

    function checkIfTrunk {
	if [ ! -d $1 ]
	then
	    echo ${1%"/trunk"}
	else
	    echo $1
	fi
    }

    galaxyHbDirFrom=$(checkIfTrunk "$hbDir/galaxy_hb_$from/trunk")
    galaxyHbDirTo=$(checkIfTrunk "$hbDir/galaxy_hb_$to/trunk")
    hbCoreDirFrom=$(checkIfTrunk "$hbDir/hb_core_$from/trunk")
    hbCoreDirTo=$(checkIfTrunk "$hbDir/hb_core_$to/trunk")
    hbCoreDirDev=$(checkIfTrunk "$hbDir/hb_core_developer/trunk")

    linkedLocalFn="$hbCoreDirFrom/config/LocalOSConfig.py"
    defaultLocalFn="$hbCoreDirFrom/config/default/LocalOSConfig.default.py"
    stableLocalFn="$hbCoreDirFrom/config/custom/LocalOSConfig.stable.py"
    testLocalFn="$hbCoreDirFrom/config/custom/LocalOSConfig.test.py"
    developerLocalFn="$hbCoreDirFrom/config/custom/LocalOSConfig.developer.py"
    codLocalFn="$hbCoreDirFrom/config/custom/LocalOSConfig.cod.py"
    mlLocalFn="$hbCoreDirFrom/config/custom/LocalOSConfig.ml.py"
    threedLocalFn="$hbCoreDirFrom/config/custom/LocalOSConfig.3d.py"
    benchLocalFn="$hbCoreDirFrom/config/custom/LocalOSConfig.bench.py"
    comparativeLocalFn="$hbCoreDirFrom/config/custom/LocalOSConfig.comparative.py"
    personalLocalFn="$hbCoreDirFrom/config/custom/LocalOSConfig.personal.py"
    snpLocalFn="$hbCoreDirFrom/config/custom/LocalOSConfig.snp.py"
    unstableLocalFn="$hbCoreDirFrom/config/custom/LocalOSConfig.unstable.py"
    multiLocalFn="$hbCoreDirFrom/config/custom/LocalOSConfig.multi.py"
    rcLocalFn="$hbCoreDirFrom/config/custom/LocalOSConfig.rc.py"
}

findCorrectDirs

function diffHeaders {
    cat $1 | cut -d ' ' -f 1 | sed -n -e '1,/^#END_DEFAULT/ s/^[A-Z_]/&/p' > "$fromTempFn"
    cat $2 | cut -d ' ' -f 1 | sed -n -e '1,/^#END_DEFAULT/ s/^[A-Z_]/&/p' > "$toTempFn"
    diff -Bu "$fromTempFn" "$toTempFn"
    diffRes="$?"

    rm "$fromTempFn"
    rm "$toTempFn"

    if [ "$diffRes" -ne "0" ]
    then
	echo "You have to fix the differences between '$1' and '$2' and run the script again."
	exit
    fi
}

diffHeaders $linkedLocalFn $defaultLocalFn
diffHeaders $defaultLocalFn $stableLocalFn
diffHeaders $stableLocalFn $testLocalFn
diffHeaders $testLocalFn $developerLocalFn
diffHeaders $developerLocalFn $codLocalFn
diffHeaders $codLocalFn $mlLocalFn
diffHeaders $mlLocalFn $threedLocalFn
diffHeaders $threedLocalFn $benchLocalFn
diffHeaders $benchLocalFn $comparativeLocalFn
diffHeaders $comparativeLocalFn $personalLocalFn
diffHeaders $personalLocalFn $snpLocalFn
diffHeaders $snpLocalFn $unstableLocalFn
diffHeaders $unstableLocalFn $multiLocalFn
diffHeaders $multiLocalFn $rcLocalFn

function checkIfSymLink {
    if [ ! -e $1 ]
    then
	echo "'$1' is not an existing symlink"
	exit
    fi
}

galaxyLinkFrom=$galaxyDir/galaxy_$from
galaxyLinkTo=$galaxyDir/galaxy_$to

checkIfSymLink $galaxyLinkFrom
checkIfSymLink $galaxyLinkTo

relFromGalaxyDir=`readlink "$galaxyLinkFrom"`
relToGalaxyDir=`readlink "$galaxyLinkTo"`
relFromGalaxyDir=`basename $relFromGalaxyDir`
relToGalaxyDir=`basename $relToGalaxyDir`

fromGalaxyDir="$galaxyDir/$relFromGalaxyDir"
toGalaxyDir="$galaxyDir/$relToGalaxyDir"

checkIfDir $fromGalaxyDir
checkIfDir $toGalaxyDir

echo "FROM: $fromGalaxyDir"
echo "TO: $toGalaxyDir"

function swap {
    echo "swap: $1 $2"
    tempFn="temp_$RANDOM"
    echo "mv $1 $tempFn"
    mv $1 $tempFn
    echo "mv $2 $1"
    mv $2 $1
    echo "mv $tempFn $2"
    mv $tempFn $2
}

function myMv {
    echo "mv: $1 $2"
    mv $1 $2
}

function myRm {
    echo "rm: $1 $2"
    rm $1 $2
}

function myLn {
    echo "ln -s: $1 $2"
    ln -s $1 $2
}

fromDate=`echo $fromGalaxyDir | sed -r 's/[^0-9]*([0-9]+).*/\1/'`
toDate=`echo $toGalaxyDir | sed -r 's/[^0-9]*([0-9]+).*/\1/'`
newFromGalaxyDir=`echo $fromGalaxyDir | sed -r "s/$fromDate/$toDate/"`
newToGalaxyDir=`echo $toGalaxyDir | sed -r "s/$toDate/$fromDate/"`

$galaxyDir/control/galaxy_$from.sh stop
$galaxyDir/control/galaxy_$to.sh stop

myMv $fromGalaxyDir $newToGalaxyDir
myMv $toGalaxyDir $newFromGalaxyDir

myRm $galaxyLinkFrom; myLn $newFromGalaxyDir $galaxyLinkFrom
myRm $galaxyLinkTo; myLn $newToGalaxyDir $galaxyLinkTo

swap $fromLocalFn $toLocalFn

$fromGalaxyWebalizerDir="$newFromGalaxyDir/static/webalizer"
$toGalaxyWebalizerDir="$newToGalaxyDir/static/webalizer"

if [ ! -e $1 ]
then
    myMv $fromGalaxyWebalizerDir $toGalaxyWebalizerDir
fi

galaxyHbDirFromMain=${galaxyHbDirFrom%"/trunk"}
galaxyHbDirToMain=${galaxyHbDirTo%"/trunk"}
hbCoreDirFromMain=${hbCoreDirFrom%"/trunk"}
hbCoreDirToMain=${hbCoreDirTo%"/trunk"}

swap $galaxyHbDirFromMain $galaxyHbDirToMain
swap $hbCoreDirFromMain $hbCoreDirToMain

findCorrectDirs

#echo "pushd .; cd $galaxyHbDirFrom/scripts/; rm hb_core; ./install.sh $hbCoreDirFrom; popd"
#pushd .; cd $galaxyHbDirFrom/scripts/; rm hb_core; ./install.sh $hbCoreDirFrom; popd
#echo "pushd .; cd $galaxyHbDirTo/scripts/; rm hb_core; ./install.sh $hbCoreDirTo; popd"
#pushd .; cd $galaxyHbDirTo/scripts/; rm hb_core; ./install.sh $hbCoreDirTo; popd

function dumpMySqlDatabase {
    user='galaxy_'$1
    pass=$2
    database=$user

    if [ $user == 'galaxy_speedtesting' ]
    then
	user='galaxy_speedtest'
    fi
    timestamp=`date +%F_%H%M`
    echo "mysqldump --user=$user --password=$pass $database > $dbDumpDir/$database-$timestamp.dump"
    mysqldump --user=$user --password=$pass $database > $dbDumpDir/$database-$timestamp.dump
}

fromPass=`cat $fromLocalFn | grep mysql | sed -r 's/.+:\/\/.+:(.+)@.*/\1/'`
toPass=`cat $fromLocalFn | grep mysql | sed -r 's/.+:\/\/.+:(.+)@.*/\1/'`
fromUrl = `cat $fromLocalFn | grep mysql | sed -r "s/.+'(.+)'.*/\1/"`

dumpMySqlDatabase $from $fromPass
dumpMySqlDatabase $to $toPass

echo "pushd .;cd $galaxyLinkFrom;sh manage_db.sh downgrade; popd"
pushd .;cd $galaxyLinkFrom;version=`sh manage_db.sh version`;sh manage_db.sh downgrade $version; popd
echo "pushd .;cd $galaxyLinkTo;sh manage_db.sh upgrade; popd"
pushd .;cd $galaxyLinkTo;sh manage_db.sh upgrade; popd

$galaxyDir/control/galaxy_$from.sh start
$galaxyDir/control/galaxy_$to.sh start
