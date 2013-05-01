# Copyright (C) 2009, Geir Kjetil Sandve, Sveinung Gundersen and Morten Johansen
# This file is part of The Genomic HyperBrowser.
#
#    The Genomic HyperBrowser is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    The Genomic HyperBrowser is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with The Genomic HyperBrowser.  If not, see <http://www.gnu.org/licenses/>.
from quick.util import GTrackConverter
import os
from quick.util.StaticFile import GalaxyRunSpecificFile

class BenchmarkCreation():
    
    def __init__(self, galaxyFn):
        self._galaxyFn = galaxyFn
    
    def _extractZipFile(self, zipfile):
        files = os.popen('tar -xzvf %s' % zipfile).readlines()
                    
        files = sorted(files)
        
        trackNames = []
        
        for i in range(1, len(files)):
            filename = files[i]
            
            trackNames.append(self._createTrackFromFileName(filename[:len(filename)-1]))
                
        return trackNames
            
    
    def _createTrackFromFileName(self, filename):
        filedata = filename.split('.')
        trackName = ''
        galaxyFile = GalaxyRunSpecificFile([filename], self._galaxyFn)
        
        currentPath = '%s/%s' % (os.getcwd(), filename)
        
        if len(filedata) == 3 and filedata[1] == 'tar' and filedata[2] == 'gz':
            os.system('mkdir %s' % galaxyFile.getDiskPath(True).split('.')[0])
            trackName = self._extractZipFile(filename)
        elif len(filedata) == 2 and filedata[1] == 'gtrack':
            os.system('cp %s %s' % (currentPath, galaxyFile.getDiskPath(True)))
            trackName = 'galaxy:gtrack:%s:None' % galaxyFile.getDiskPath(True)
        else:
            raise Exception('%s is not in a valid format' % filename)
        
        return trackName
    
    def downloadFileFromURL(self, url):
        data = url.split('/')
        filename = data[len(data)-1]
        os.system('wget %s > /dev/null 2>&1' % url)

        if os.path.exists(filename):
            return self._createTrackFromFileName(filename)
        else:
            raise Exception('%s does not exist' % filename)
    
    def handleHistoryItem(self, trackName):
        trackData = trackName.split(':')
        fileFormat = trackData[1]
            
        if fileFormat != 'gtrack':
            gtconverter = GTrackConverter()
            trackData[2] = gtconverter.convertToGTrack(trackData[2], fileFormat, self._galaxyFn)
            trackData[1] = 'gtrack'
            
        return trackName
        