import os
from numpy import *
from gold.application.GalaxyInterface import GalaxyInterface
from gold.application.StatRunner import AnalysisDefJob
from quick.webtools.GeneralGuiTool import GeneralGuiTool
from Pycluster import *
from test.sandbox.master.draw_dendrogram import draw_dendrogram
from quick.util.StaticFile import StaticFile

#from quick.application.GalaxyInterface import getAllGenomes

#This is a template prototyping GUI that comes together with a corresponding web page.

        
        
class EivindGLsTool(GeneralGuiTool):
    @staticmethod
    def getToolName():
        return "Hieps tool.."

    @staticmethod
    def getInputBoxNames(prevChoices=None):
        "Returns a list of names for input boxes, implicitly also the number of input boxes to display on page. Each such box will call function getOptionsBoxK, where K is in the range of 1 to the number of boxes"
        return ['repeat1', 'repeat2', 'repeat3'] #, 'repeat4', 'repeat5', 'repeat6']
    @staticmethod    
    def getOptionsBox1():
        "Returns a list of options to be displayed in the first options box"
        return ['DNA','LINE','SINE','Satellite','rRNA','LTR']
    
    @staticmethod    
    def getOptionsBox2(prevChoices): 
        '''Returns a list of options to be displayed in the second options box, which will be displayed after a selection is made in the first box.
        prevChoices is a list of selections made by the web-user in the previous input boxes (that is, list containing only one element for this case)        
        '''
        #if prevChoices[0] == 'testChoice1' :
        #    return ['testbox2_choice1-1','testbox2_choice1-2']
        #else :
        #    return ['testbox2_choice2-1','testbox2_choice2-2']
        return ['DNA','LINE','SINE','Satellite','rRNA','LTR']
    
    @staticmethod    
    def getOptionsBox3(prevChoices):
        return ['DNA','LINE','SINE','Satellite','rRNA','LTR']
    '''
    @staticmethod    
    def getOptionsBox4(prevChoices):
        return ['DNA','LINE','SINE','Satellite','rRNA','LTR']
        
    @staticmethod    
    def getOptionsBox5(prevChoices):
        return ['DNA','LINE','SINE','Satellite','rRNA','LTR']

    @staticmethod    
    def getOptionsBox6(prevChoices):
        return ['DNA','LINE','SINE','Satellite','rRNA','LTR']
    '''
        
    @staticmethod
    def computeDistance(track1, track2, feature='direct distance'):
        '''
        track1 and track2 are two lists like : ['Sequence','Repeating elements','LINE']
        feature specifies how the distance between track1 and track2 is defined 
        '''
        analysisDef = 'bla bla -> PropFreqOfTr1VsTr2Stat' #or any other statistic from the HB collection
        regSpec = 'chr1' #could also be e.g. 'chr1' for the whole chromosome or '*' for the whole genome
        binSpec = '10m' #could also be e.g.'100', '1k' or '*' for whole regions/chromosomes as bins 
        genome = 'hg18' # path /../../..../genome
        #allRepeats = GalaxyInterface.getSubTrackNames(genome,['Sequence','Repeating elements'],False) #all elements in 'Repeating elements' directory
        #GalaxyInterface.run(trackName1, trackName2, question, regSpec, binSpec, genome='hg18')
        userBinSource = GalaxyInterface._getUserBinSource(regSpec,binSpec,genome)
        
        result = AnalysisDefJob(analysisDef, track1, track2, userBinSource).run()
        #result er av klassen Results..
        #from gold.result.Results import Results

        mainResultDict = result.getGlobalResult()
        #from PropFreqOfTr1VsTr2Stat:...
        #self._result = {'Track1Prop':ratio,'CountTrack1':c1, 'CountTrack2':c2,'Variance':variance}

        mainValueOfInterest = mainResultDict['Variance']
        return mainValueOfInterest
        
    @staticmethod
    def constructDistMatrix(tracks):
        l = len(tracks)
        matrix = zeros((l,l))
        for i in range(l) :
            for j in range(l):
                if i < j :
                    matrix[i,j] = HiepsTool.computeDistance(tracks[i],tracks[j])
                    matrix[j,i] = matrix[i,j] 
        return matrix
        
    @staticmethod    
    def execute(choices, galaxyFn=None, username=''):
        '''Is called when execute-button is pushed by web-user.
        Should print output as HTML to standard out, which will be directed to a results page in Galaxy history.
        If needed, StaticFile can be used to get a path where additional files can be put (e.g. generated image files).
        choices is a list of selections made by web-user in each options box.
        '''
        
        #print 'Executing...'    
        #print choices   
        #trackName1 = ['Sequence','Repeating elements','LINE'] #a list of subdirectories from 'genome' to the repeat file
        #trackName2 = ['Sequence','Repeating elements','SINE']
        #allRepeats = GalaxyInterface.getSubTrackNames(genome,['Sequence','Repeating elements'],False) #all elements in 'Repeating elements' directory
        
        #analysisDef = 'bla bla -> PropFreqOfTr1VsTr2Stat' #or any other statistic from the HB collection
        #regSpec = 'chr1' #could also be e.g. 'chr1' for the whole chromosome or '*' for the whole genome
        #binSpec = '10m' #could also be e.g.'100', '1k' or '*' for whole regions/chromosomes as bins 
        genome = 'hg18' # path /../../..../genome
        allRepeats = GalaxyInterface.getSubTrackNames(genome,['Sequence','Repeating elements'],False) #all elements in 'Repeating elements' directory
        #GalaxyInterface.run(trackName1, trackName2, question, regSpec, binSpec, genome='hg18')
        #userBinSource = GalaxyInterface._getUserBinSource(regSpec,binSpec,genome)

        #result = AnalysisDefJob(analysisDef, trackName1, trackName2, userBinSource).run()
        #result er av klassen Results..
        #from gold.result.Results import Results

        #mainResultDict = result.getGlobalResult()
        #from PropFreqOfTr1VsTr2Stat:...
        #self._result = {'Track1Prop':ratio,'CountTrack1':c1, 'CountTrack2':c2,'Variance':variance}

        #mainValueOfInterest = mainResultDict['Variance']
        
        #print 'first repeat', allRepeats[0]
        #print '\n all repeats', allRepeats
        #minValue = HiepsTool.computeDistance(trackName1,trackName2)
        #print minValue
        #choicedTracks = [['Sequence','Repeating elements',name] for name in choices]
        #print '\n choiced tracks', choicedTracks
        #d_matrix = HiepsTool.constructDistMatrix(choicedTracks)
        #tree = treecluster(distancematrix=d_matrix, method='s')
        #print tree

        #figure = StaticFile(['hiepln','dendro'],'jpg')
        #filepath = figure.getDiskPath()
        #print filepath           
        #draw_dendrogram(tree,choices,filepath)
        #print figure.getLink('clustring result')
        
        track1 = ['Sequence','Repeating elements', 'DNA']
        track2 = ['Gene regulation', 'TFBS', 'High Throughput']
        analysisDef = 'bla bla -> DerivedOverlapStat' #or any other statistic from the HB collection
        regSpec = 'chr1' #could also be e.g. 'chr1' for the whole chromosome or '*' for the whole genome
        binSpec = '10m' #could also be e.g.'100', '1k' or '*' for whole regions/chromosomes as bins 
        genome = 'hg18' # path /../../..../genome
        #allRepeats = GalaxyInterface.getSubTrackNames(genome,['Sequence','Repeating elements'],False) #all elements in 'Repeating elements' directory
        #GalaxyInterface.run(trackName1, trackName2, question, regSpec, binSpec, genome='hg18')
        userBinSource = GalaxyInterface._getUserBinSource(regSpec,binSpec,genome)
        
        result = AnalysisDefJob(analysisDef, track1, track2, userBinSource).run()
        #result er av klassen Results..
        #from gold.result.Results import Results

        mainResultDict = result.getGlobalResult()
        #keys = result.getResDictKeys()
        #print keys
        #print mainResultDict['2in1']
        print '<ol>'
        for key in mainResultDict.keys() : 
            print '<li>key:%s,value:%s </li>'%(key,mainResultDict[key])
        print '</ol>'
    
