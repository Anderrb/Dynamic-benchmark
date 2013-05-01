if [ $# -ne 1 ]
then
    echo "usage:   packAndReleaseCode.sh version"
    echo "example: release.sh v1.0"
    exit
fi

version="$1"
coreDir="GenomicHyperBrowser_"$version"_core"
guiDir="GenomicHyperBrowser_"$version"_gui"

sourceDir='/usit/invitro/data/hyperbrowser/galaxy_hb_stable/trunk/static/hyperbrowser/source'

svn co "file:///projects/bioinfoprojects/svn_repository/new_hb/tags/release-$1" $coreDir
svn co "file:///projects/bioinfoprojects/svn_repository/galaxy_hb/tags/release-$1" $guiDir

function removeSvnDirs {
    pushd .
    cd $1
    rm -rf `find . -name .svn`
    popd
}

function checkIfDir {
    if [ ! -d $1 ]
    then
	echo "'$1' is not an existing directory"
	exit
    fi
}

checkIfDir $coreDir
checkIfDir $guiDir
checkIfDir $sourceDir

removeSvnDirs $coreDir
removeSvnDirs $guiDir

rm $coreDir/data/CommandCatalog.shelve
rm $coreDir/data/profiles*
rm $coreDir/data/TrackInfo.shelve

rm $guiDir/static/hyperbrowser/videos/*
rm $guiDir/static/hyperbrowser/source/*
rm -R $guiDir/static/hyperbrowser/images/origs
rm -R $guiDir/static/hyperbrowser/images/old
rm -R $guiDir/static/hyperbrowser/notes/stats/old
rm -R $guiDir/static/hyperbrowser/notes/stats/in_progress

tar cfzv "$sourceDir/$coreDir.tar.gz" $coreDir
tar cfzv "$sourceDir/$guiDir.tar.gz" $guiDir

rm -R $coreDir
rm -R $guiDir

cd $sourceDir
svn add "$coreDir.tar.gz"
svn add "$guiDir.tar.gz"
svn commit -m 'Zipped source code added for version: $version'
pwd -P
popd