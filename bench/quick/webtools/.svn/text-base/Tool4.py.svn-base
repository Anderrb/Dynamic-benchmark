from quick.webtools.GeneralGuiTool import GeneralGuiTool
from quick.util.StaticFile import RunSpecificPickleFile
import pkg_resources
from quick.aux.TrackExtractor import TrackExtractor
pkg_resources.require('PIL')
import Image
from collections import defaultdict
from quick.util.StaticFile import GalaxyRunSpecificFile
from quick.application.ExternalTrackManager import ExternalTrackManager
from gold.result.HtmlCore import HtmlCore
from quick.application.GalaxyInterface import GalaxyInterface
from quick.application.UserBinSource import UserBinSource
from gold.origdata.GtrackGenomeElementSource import GtrackGenomeElementSource
from gold.track.GenomeRegion import GenomeRegion
from quick.util.GenomeInfo import GenomeInfo

# This is a template prototyping GUI that comes together with a corresponding
# web page.

class Tool4(GeneralGuiTool):
    @staticmethod
    def getToolName():
        '''
        Specifies a header of the tool, which is displayed at the top of the
        page.
        '''
        return "Benchmark retrieval tool"

    @staticmethod
    def getInputBoxNames():
        '''
        Specifies a list of headers for the input boxes, and implicitly also the
        number of input boxes to display on the page. The returned list can have
        two syntaxes:
        
            1) A list of strings denoting the headers for the input boxes in
               numerical order.
            2) A list of tuples of strings, where each tuple has
               two items: a header and a key.
        
        The contents of each input box must be defined by the function
        getOptionsBoxK, where K is either a number in the range of 1 to the
        number of boxes (case 1), or the specified key (case 2).
        '''
        return ['Select benchmark:'] #Alternatively: [ ('box1','1'), ('box2','2') ]

    #@staticmethod
    #def getInputBoxOrder():
    #    '''
    #    Specifies the order in which the input boxes should be displayed, as a
    #    list. The input boxes are specified by index (starting with 1) or by
    #    key. If None, the order of the input boxes is in the order specified by
    #    getInputBoxNames.
    #    '''
    #    return None
    
    @staticmethod    
    def getOptionsBox1(): # Alternatively: getOptionsBoxKey()
        '''
        Defines the type and contents of the input box. User selections are
        returned to the tools in the prevChoices and choices attributes to other
        methods. These are lists of results, one for each input box (in the
        order specified by getInputBoxOrder()).
        
        The input box is defined according to the following syntax:
        
        Selection box:          ['choice1','choice2']
        - Returns: string
        
        Text area:              'textbox' | ('textbox',1) | ('textbox',1,False)
        - Tuple syntax: (contents, height (#lines) = 1, read only flag = False)
        - Returns: string
        
        Password field:         '__password__'
        - Returns: string
        
        Genome selection box:   '__genome__'
        - Returns: string
        
        Track selection box:    '__track__'
        - Requires genome selection box.
        - Returns: colon-separated string denoting track name
        
        History selection box:  ('__history__',) | ('__history__', 'bed', 'wig')
        - Only history items of specified types are shown.
        - Returns: colon-separated string denoting galaxy track name, as
                   specified in ExternalTrackManager.py.
        
        History check box list: ('__multihistory__', ) | ('__multihistory__', 'bed', 'wig')
        - Only history items of specified types are shown.
        - Returns: OrderedDict with galaxy track name as key and selection
                   status (bool) as value.
        
        Hidden field:           ('__hidden__', 'Hidden value')
        - Returns: string
        
        Table:                  [['header1','header2'], ['cell1_1','cell1_2'], ['cell2_1','cell2_2']]
        - Returns: None
        
        Check box list:         OrderedDict([('key1', True), ('key2', False), ('key3', False)])
        - Returns: OrderedDict from key to selection status (bool).
        '''
        return ('__history__',)
#    
#    @staticmethod    
#    def getOptionsBox2(prevChoices): 
#        '''
#        See getOptionsBox1().
#        
#        prevChoices is a namedtuple of selections made by the user in the
#        previous input boxes (that is, a namedtuple containing only one element
#        in this case). The elements can accessed either by index, e.g.
#        prevChoices[0] for the result of input box 1, or by key, e.g.
#        prevChoices.key (case 2).
#        '''
#        return ''
        
    #===========================================================================
    # @staticmethod    
    # def getOptionsBox3(prevChoices):
    #    return '__track__'
    #    
    #===========================================================================
    #@staticmethod    
    #def getOptionsBox4(prevChoices):
    #    return ['']

    #@staticmethod
    #def getDemoSelections():
    #    return ['testChoice1','..']
        
    @classmethod    
    def execute(cls, choices, galaxyFn=None, username=''):
        '''
        Is called when execute-button is pushed by web-user. Should print
        output as HTML to standard out, which will be directed to a results page
        in Galaxy history. If getOutputFormat is anything else than HTML, the
        output should be written to the file with path galaxyFn. If needed,
        StaticFile can be used to get a path where additional files can be put
        (e.g. generated image files). choices is a list of selections made by
        web-user in each options box.
        '''
        
        try:
            historyInputTN = choices[0].split(':') #from history
            historyGalaxyFn = ExternalTrackManager.extractFnFromGalaxyTN( historyInputTN) #same as galaxyFn in execute of create benchmark..
            randomStatic = RunSpecificPickleFile(historyGalaxyFn) #finds path to static file created for a previous history element, and directs to a pickle file
            myInfo = randomStatic.loadPickledObject()
        except:
            return None
        
        galaxyTN = myInfo[3].split(':')
        myFileName = ExternalTrackManager.extractFnFromGalaxyTN(galaxyTN)
        genome = myInfo[0]
        
        gtrackSource = GtrackGenomeElementSource(myFileName, genome)
        regionList = []
        
        for obj in gtrackSource:
            regionList.append(GenomeRegion(obj.genome, obj.chr, obj.start, obj.end))
        
        extractor = TrackExtractor()
                
        fn = extractor.extract(GenomeInfo.getSequenceTrackName(genome), regionList, galaxyFn, 'fasta')
            
            
        
    @staticmethod
    def validateAndReturnErrors(choices):
        '''
        Should validate the selected input parameters. If the parameters are not
        valid, an error text explaining the problem should be returned. The GUI
        then shows this text to the user (if not empty) and greys out the
        execute button (even if the text is empty). If all parameters are valid,
        the method should return None, which enables the execute button.
        '''
        return None
    
    @classmethod
    def getSubResult(cls, start, end, realNum, rows, cols):
        #print start, end
        if end-start == rows*cols:
            tempRes = [range(start+cols*i,min(realNum, start+cols*(i+1))) if start+cols*i < realNum else [] for i in range(rows)]
            return tempRes
            
            
        elif end-start > rows*cols:
            addition = int((end-start)/4)
            
            res1 = cls.getSubResult(start, start+addition, realNum, rows, cols)
            res2 = cls.getSubResult(start+addition, start+addition*2, realNum, rows, cols)
            res3 = cls.getSubResult(start+addition*2, start+addition*3, realNum, rows, cols)
            res4 = cls.getSubResult(start+addition*3, start+addition*4, realNum, rows, cols)
            
            entries = len(res1)
            result = [[] for v in range(entries*2)]
            counter=0
            for resTuple in [(res1,res2),(res3,res4)]:
                for index in range(entries):
                    result[counter] += resTuple[0][index]+resTuple[1][index]
                    counter+=1
            return result
    
    @classmethod
    def getResult(cls, numEntries, rows, cols):
        expandedEntries = rows*cols
        while expandedEntries< numEntries:
            expandedEntries*=4
            
        res = [row for row in cls.getSubResult(0, expandedEntries, numEntries, rows, cols) if row !=[]]
        return res
    
    @classmethod
    def getValuesFromBedFile(cls, fn, colorPattern=(1,0,0)):
        resDict = defaultdict(list)
        count=0
        for line in open(fn,'r'):
            count+=1
            lineTab = line.split('\t')
            chrom = lineTab[0]
            try:
                value = int(float(lineTab[3])*255)
                resDict[chrom]+= [tuple([value*v for v in colorPattern])]
            except:
                print lineTab
        #print 'count', count
        return resDict
    
    @classmethod
    def syncResultDict(cls, resultDicts):
        newResult = defaultdict(list)
        for chrom in resultDicts[0].keys():
            valLists = [v[chrom] for v in resultDicts]
            
            for elemIndex in range(len(valLists[0])):
                color = None
                tempRes = []
                for valListIndx in range(len(valLists)):
                    tempRes.append(valLists[valListIndx][elemIndex])
                #print tempRes
                color = tuple([max(v) for v in zip(*tempRes)])
                newResult[chrom]+=[color]
        return newResult
    
    @classmethod
    def MakeHeatmapFromTracks(cls, galaxyFn, **trKwArgs):
        tr1 = trKwArgs.get('tr1')
        tr2 = trKwArgs.get('tr2')
        tr3 = trKwArgs.get('tr3')
        tableRowEntryTemplate = """<tr><td>%s</td><td><a href="%s"><img src="%s" /></a></td></tr>"""
        #htmlTemplate = '''<head><link rel="stylesheet" type="text/css" href="image_zoom/styles/stylesheet.css" /><script language="javascript" type="text/javascript" src="image_zoom/scripts/mootools-1.2.1-core.js"></script><script language="javascript" type="text/javascript" src="image_zoom/scripts/mootools-1.2-more.js"></script><script language="javascript" type="text/javascript" src="image_zoom/scripts/ImageZoom.js"></script>
        #                <script language="javascript" type="text/javascript" >
        #                liste = %s;
        #                function point_it(event){
        #                        pos_x = event.offsetX?(event.offsetX):event.pageX-document.getElementById("zoomer_image").offsetLeft;
        #                        pos_y = event.offsetY?(event.offsetY):event.pageY-document.getElementById("zoomer_image").offsetTop;
        #                        pos_x = Math.floor(pos_x/10);
        #                        pos_y = Math.floor(pos_y/10);
        #                        alert("Hello World!, you clicked: " +liste[pos_y][pos_x]);
        #                }</script>
        #                </head><body><div id="container"><!-- Image zoom start --><div id="zoomer_big_container"></div><div id="zoomer_thumb">		<a href="%s" target="_blank" ><img src="%s" /></a></div><!-- Image zoom end --></div></body></html>'''
        javaScriptCode = '''
liste = %s;
    function point_it(event){
            pos_x = event.offsetX?(event.offsetX):event.pageX-document.getElementById("zoomer_image").offsetLeft;
            pos_y = event.offsetY?(event.offsetY):event.pageY-document.getElementById("zoomer_image").offsetTop;
            pos_x = Math.floor(pos_x/10);
            pos_y = Math.floor(pos_y/10);
            alert("Hello World!, you clicked: " +liste[pos_y][pos_x]);
    }
'''

        
        
        ResultDicts = [cls.getValuesFromBedFile(tr1,colorPattern=(1,0,0))]
        ResultDicts += [cls.getValuesFromBedFile(tr2,colorPattern=(0,1,0))] if tr2 else []
        ResultDicts += [cls.getValuesFromBedFile(tr3,colorPattern=(0,0,1))] if tr3 else []
    
    
        htmlTableContent = []
        resultDict = cls.syncResultDict(ResultDicts)
        
        for chrom, valList in resultDict.items():
            areaList = []
            #For doing recursive pattern picture
            posMatrix = cls.getResult(len(valList), 2,2)
            javaScriptList = [[0 for v in xrange(len(posMatrix[0])) ] for t in xrange(len(posMatrix))]
            rowLen = len(posMatrix[0])
            im = Image.new("RGB", (rowLen, len(posMatrix)), "white")
            for yIndex, row in enumerate(posMatrix):
                for xIndex, elem in enumerate(row):
                    im.putpixel((xIndex, yIndex), valList[elem])
                    region = yIndex*rowLen + xIndex
                    javaScriptList[yIndex][xIndex] = chrom+':'+str(elem*10)+'-'+str((elem+1)*10)+': '+repr([ round((255-v)/255.0 ,2 ) for v in valList[elem]])
                    #areaList.append(areaTemplate % (xIndex*10, yIndex*10, xIndex*11, yIndex*11, repr(valList[elem])))
            im2 = im.resize((len(posMatrix[0])*10, len(posMatrix)*10))
            
            origSegsFile = GalaxyRunSpecificFile([chrom+'smallPic.png'], galaxyFn)
            origSegsFn = origSegsFile.getDiskPath(True)
            bigSegsFile = GalaxyRunSpecificFile([chrom+'BigPic.png'], galaxyFn)
            bigSegsFn = bigSegsFile.getDiskPath(True)
            
            im.save(origSegsFn)
            im2.save(bigSegsFn)
            
            
            #open('Recursive/'+chrom+'Zooming.html','w').write(htmlTemplate % (str(javaScriptList), chrom+'Big.png',chrom+'.png'))
            core = HtmlCore()
            core.begin( extraJavaScriptFns=['mootools-1.2.1-core.js', 'mootools-1.2-more.js', 'ImageZoom.js'], extraJavaScriptCode=javaScriptCode % str(javaScriptList), extraCssFns=['image_zoom.css'] )
            core.styleInfoBegin(styleId='container')
            core.styleInfoBegin(styleId='zoomer_big_container')
            core.styleInfoEnd()
            core.styleInfoBegin(styleId='zoomer_thumb')
            core.link(url=bigSegsFile.getURL(), text=str(HtmlCore().image(origSegsFile.getURL())), popup=True)
            core.styleInfoEnd()
            core.styleInfoEnd()
            core.end()
            htmlfile = GalaxyRunSpecificFile([chrom+'.html'], galaxyFn)
            htmlfile.writeTextToFile(str(core))
            htmlTableContent.append(tableRowEntryTemplate % (chrom, htmlfile.getURL(), origSegsFile.getURL()))
            
            #return str(core)  #htmlTemplate % (str(javaScriptList), bigSegsFn, origSegsFn)
        
            #######
            
            # FOr doing normal picture
            #columns = int(round((len(valList)/1000)+0.5))
            #im = Image.new("RGB", (1000, columns), "white")        
            #y=-1    
            #for index, valuTuple in enumerate(valList):
            #    x = index%1000
            #
            #    if x == 0:
            #        y+=1
            #    try:
            #        im.putpixel((x, y), valuTuple)
            #    except:
            #        pass
            #im.save(chrom+'.png')
            #htmlTableContent.append(tableRowEntryTemplate % (chrom, chrom+'.png'))
        htmlPageTemplate = """<html><body><table border="1">%s</table></body></html>"""
        return htmlPageTemplate % ('\n'.join(htmlTableContent))
        #open('Recursive/ChromosomeImages.html','w').write())
    
    #
    

        
    #@staticmethod
    #def getSubToolClasses():
    #    '''
    #    Specifies a list of classes for subtools of the main tool. These
    #    subtools will be selectable from a selection box at the top of the page.
    #    The input boxes will change according to which subtool is selected.
    #    '''
    #    return None
    #
    #@staticmethod
    #def isPublic():
    #    '''
    #    Specifies whether the tool is accessible to all users. If False, the
    #    tool is only accessible to a restricted set of users as defined in
    #    LocalOSConfig.py.
    #    '''
    #    return False
    #
    #@staticmethod
    #def isRedirectTool():
    #    '''
    #    Specifies whether the tool should redirect to an URL when the Execute
    #    button is clicked.
    #    '''
    #    return False
    #
    #@staticmethod
    #def getRedirectURL(choices):
    #    '''
    #    This method is called to return an URL if the isRedirectTool method
    #    returns True.
    #    '''
    #    return ''
    #
    #@staticmethod
    #def isHistoryTool():
    #    '''
    #    Specifies if a History item should be created when the Execute button is
    #    clicked.
    #    '''
    #    return True
    #
    #@staticmethod
    #def isDynamic():
    #    '''
    #    Specifies whether changing the content of texboxes causes the page to
    #    reload.
    #    '''
    #    return True
    #
    #@staticmethod
    #def getResetBoxes():
    #    '''
    #    Specifies a list of input boxes which resets the subsequent stored
    #    choices previously made. The input boxes are specified by index
    #    (starting with 1) or by key.
    #    '''
    #    return []
    #
    #@staticmethod
    #def getToolDescription():
    #    '''
    #    Specifies a help text in HTML that is displayed below the tool.
    #    '''
    #    return ''
    #
    #@staticmethod
    #def getToolIllustration():
    #    '''
    #    Specifies an id used by StaticFile.py to reference an illustration file
    #    on disk. The id is a list of optional directory names followed by a file
    #    name. The base directory is STATIC_PATH as defined by AutoConfig.py. The
    #    full path is created from the base directory followed by the id.
    #    '''
    #    return None
    #
    #@classmethod
    #def isBatchTool(cls):
    #    '''
    #    Specifies if this tool could be run from batch using the batch. The
    #    batch run line can be fetched from the info box at the bottom of the
    #    tool.
    #    '''
    #    return cls.isHistoryTool()
    #
    #@staticmethod
    #def isDebugMode():
    #    '''
    #    Specifies whether debug messages are printed.
    #    '''
    #    return False
    #
    
    @staticmethod    
    def getOutputFormat(choices):
        '''
        The format of the history element with the output of the tool. Note
        that html output shows print statements, but that text-based output
        (e.g. bed) only shows text written to the galaxyFn file.In the latter
        case, all all print statements are redirected to the info field of the
        history item box.
        '''
        return 'customhtml'
    