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
import os
from quick.util.StaticFile import GalaxyRunSpecificFile
from quick.util.GTrackConverter import GTrackConverter
from quick.application.ExternalTrackManager import ExternalTrackManager
from gold.origdata.GtrackGenomeElementSource import GtrackGenomeElementSource
from gold.track.GenomeRegion import GenomeRegion
from quick.util.GenomeInfo import GenomeInfo
from quick.aux.TrackExtractor import TrackExtractor
from quick.application.GalaxyInterface import GalaxyInterface

'''
Utility class for the benchmarking tools.
'''
class BenchmarkUtil():
    
    def __init__(self, galaxyFn, genome):
        
        self._galaxyFn = galaxyFn
        self._genome = genome
        self._extractor = TrackExtractor()
    
    '''
    Given a filename, this function finds out what kind of file we are dealing with.
    
    PARAMETERS
    
    filename: string containing the name of the file
    
    RETURNS
    
    A string containing the type of the filename given in parameters
    '''
    def _findFileType(self, filename):
        
        filedata = filename.split('.')
        
        if os.path.isdir(filename):
            return 'directory'
        elif filedata[-2] == 'tar' and filedata[-1] == 'gz':  
            return 'tar'
           
        fileheader = open(filename, 'r').readlines(5)
        
        if filedata[-1] == 'gtrack':
            return 'gtrack'
        elif filedata[-1] == 'wee':
            return 'weeder'
        elif fileheader[0] == '# blastn\n':
            return 'blasthit'
        elif fileheader[1] == 'MEME - Motif discovery tool\n':
            return 'meme'
        elif fileheader[0][:10] == 'DEFINITION' and fileheader[1][:8] == 'FEATURES':
            return 'prodigal'
        elif filedata[-1] =='predict':
            return 'glimmer'
        elif fileheader[0][:8] == 'The best':
            return 'ymf'
         
        return None
    
    '''
    Extracts a zip archive and tries to create track names from its content.
    
    PARAMETERS
    
    zipFilePath: string containing the complete path to a zip file
    
    RETURNS
    
    trackNames:       list of strings containing track names of the content within the zip archive
    '''
    def _extractZipFile(self, zipFilePath):
        
        extractedFiles = os.popen('tar -xzvf %s' % zipFilePath).readlines()
        extractedFiles = sorted(extractedFiles)
        trackNames = []
        
        # For every extracted file...
        for i in range(1, len(extractedFiles)):
            filepath = '%s/%s' % (os.getcwd(), extractedFiles[i][:len(extractedFiles[i])-1])
            
            # Try to create a track names from the extracted files path
            if os.path.isfile(filepath):
                trackNames.append(self._createTrackFromDownloadedFile(filepath))
                
        return trackNames
    
    '''
    Creates one or more track names from the file path of a downloaded file.
    
    PARAMATERS
    
    filepath: string containing the path of the downloaded file
    
    RETURNS
    
    trackName:    can either be a string containing a single track name or a list
                  containing all the track names within a zip archive
    '''
    def _createTrackFromDownloadedFile(self, filepath):
        
        trackName = ''
        filename = filepath.split('/')[-1]
        galaxyFile = GalaxyRunSpecificFile([filename], self._galaxyFn)
        
        # Find the file type of downloaded file
        fileType = self._findFileType(filepath)
        
        if fileType == None:
            # If invalid file type, raise an exception
            raise Exception('%s is not in a valid format' % filepath)
        elif fileType == 'directory':
            
            trackName = None
        elif fileType == 'tar': 
            # If its a zip file, extract it
            os.system('mkdir %s' % galaxyFile.getDiskPath(True).split('.')[0])
            trackName = self._extractZipFile(filepath)
        else: 
            # If its a valid trackName file, copy it and create a trackName
            os.system('cp %s %s' % (filepath, galaxyFile.getDiskPath(True)))
            trackName = 'galaxy:%s:%s:None' % (fileType, galaxyFile.getDiskPath())
        
        return trackName
    
    '''
    Downloads a file with wget command from a given URL. If the URL is valid go on to process the downloaded file.
    
    PARAMETERS
    
    url:    string containing an url to the file to be downloaded
    
    RETURNS
    
    A string with a single track name, or a list containing several track names
    '''
    def downloadFileFromURL(self, url):
        
        data = url.split('/')
        filename = data[-1]
        os.system('wget %s > /dev/null 2>&1' % url)
        filepath = '%s/%s' % (os.getcwd(), filename)
        
        if os.path.exists(filename):
            return self._createTrackFromDownloadedFile(filepath)
        else:
            raise Exception('%s does not exist' % filename)
    
    '''
    Checks the file type of a given track name, and converts it to GTrack if necessary.
    
    PARAMETERS
    
    trackName:       string containing the track name which is to be converted to GTrack
    regionTrack:     string containing a track name specifying the region boundaries of the track
    
    RETURNS
    
    trackName:   string containing a track name in GTrack format
    fileFormat:  string containing the original file format, 
                 which can be used later for naming an algorithm
    '''
    def convertToGTrack(self, trackName, regionTrackName=None, gtconverter=None, normalizeValues=False):
        
        trackData = trackName.split(':')
        fileFormat = trackData[1]
        
        if gtconverter == None:
            gtconverter = GTrackConverter()
        
        
        
        if not fileFormat == 'gtrack' or normalizeValues == True: 
            # If the file is in a format which requires the original fasta sequence
            if fileFormat == 'ymf':
                # First retrieve the fasta file, then go ahead and convert to GTrack
                fastaFile = GalaxyRunSpecificFile(['tmp.fasta'], self._galaxyFn)
                self.retrieveTrack(regionTrackName, fastaFile.getDiskPath(True))
                
                trackData[2] = gtconverter.convertToGTrack(trackData[2], 
                                fileFormat, self._galaxyFn, fastaFilePath=fastaFile.getDiskPath())
                
                trackData[1] = 'gtrack'
            else:
                trackData[2] = gtconverter.convertToGTrack(trackData[2], 
                                fileFormat, self._galaxyFn, normalizeValues=normalizeValues)
                
                trackData[1] = 'gtrack'
                
            trackName = '%s:%s:%s:%s' % (trackData[0], trackData[1], trackData[2], trackData[3])
            
        return trackName, fileFormat
    
    '''
    Converts a dictionary containing prediction track names to GTrack.
    
    PARAMETERS
    
    predictionDict: dictionary of prediction track name strings
    regionTracks:   list of region track name strings
    
    RETURNS
    
    predictionDict: dictionary of prediction GTrack strings
    algorithmNames: list of extracted algorithm names from prediction track strings
    '''
    def convertPredictionDictionaryToGTrack(self, predictionDict, regionTrackName, normalizeValues=False):
        
        regionIndex = 0
        algorithmNames = []
        gtconverter = GTrackConverter()

        for key, predictionTrackName in predictionDict.items():
            
            predictionDict[key], algorithmName = self.convertToGTrack(predictionTrackName, 
                                        regionTrackName, gtconverter, normalizeValues)
            
            algorithmNames.append(algorithmName)
            regionIndex = regionIndex + 1
        
        return predictionDict, algorithmNames
    
    '''
    Converts a dictionary containing prediction track names to GTrack.
    
    PARAMETERS
    
    predictionList: list of prediction track name strings
    regionTracks:   list of region track name strings
    
    RETURNS
    
    predictionList: list of prediction GTrack strings
    algorithmNames: list of extracted algorithm names from prediction track strings
    '''
    def convertPredictionListToGTrack(self, predictionList, regionTrackNames, normalizeValues=False):
        
        algorithmNames = []
        nRegions = len(regionTrackNames)
        gtconverter = GTrackConverter()
        
        for i in range(0, len(predictionList)):
            
            predictionList[i], algorithmName = self.convertToGTrack(predictionList[i], 
                                                    regionTrackNames[i%nRegions], gtconverter, normalizeValues=normalizeValues)
            
            algorithmNames.append(algorithmName)
        
        return predictionList, algorithmNames
    
    '''
    Extracts sequences as a fasta file based on a given track name.
    
    PARAMETERS
    
    trackName: string containing the track to be retrieved
    
    RETURNS
    
    A track name referring to a fasta file containing the sequences specified by trackName
    '''
    def retrieveTrack(self, regionTrackName, fastaFileName):
        
        regionTrackName = regionTrackName.split(':')
        myFileName = ExternalTrackManager.extractFnFromGalaxyTN(regionTrackName)
        gtrackSource = GtrackGenomeElementSource(myFileName, self._genome)
        regionList = []
        
        for obj in gtrackSource:
            regionList.append(GenomeRegion(obj.genome, obj.chr, obj.start, obj.end))
        
        return self._extractor.extract(GenomeInfo.getSequenceTrackName(self._genome), regionList, fastaFileName, 'fasta')
    
    '''
    Retrieves a feature track  
    '''
    def retrieveFeatureTrack(self, genome, galaxyFn, regionTrackName, featureTrack):
        
        regionTrackName = regionTrackName.split(':')
        regionFileName = ExternalTrackManager.extractFnFromGalaxyTN(regionTrackName)
        
        bins = GalaxyInterface._getUserBinSource('gtrack', regionFileName, genome, featureTrack.split(':'))
        
        return self._extractor.extract(featureTrack.split(':'), bins, galaxyFn, 'gtrack')
    
    '''
    Extract an entire set of fasta files and save it to a zip archive.
    
    PARAMETERS
    
    trackNames: list of strings containing track names to be retrieved as fasta
    
    RETURNS
    
    A string containing a link to the zip archive
    '''
    def retrieveBenchmarkSuiteAsZipFile(self, trackNames):
        zipFile = GalaxyRunSpecificFile(['BenchmarkSuite.tar.gz'], self._galaxyFn)
        path = zipFile.getDiskPath(True)
        path =  path[0:-len(path.split('/')[-1])]
            
        # For every trackName, retrieve the trackName and copy it to a directory
        for trackName in trackNames:
            filePath = trackName.split(':')[2].split('/')
            fileName = filePath[len(filePath)-1]
            fastaFileName = GalaxyRunSpecificFile(['BenchmarkSuite/%s.fasta' % fileName.split('.')[0]], self._galaxyFn)
            self.retrieveTrack(trackName, fastaFileName.getDiskPath(True))
            
        # And finally create a zip file, and return a link pointing to it
        os.system('tar -P -czvf %sBenchmarkSuite.tar.gz %sBenchmarkSuite/' % (path, path))
            
        return zipFile.getLink("Download benchmark suite")
    