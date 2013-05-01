from quick.webtools.GeneralGuiTool import GeneralGuiTool
from config.LocalOSConfig import *
import os

class GenerateTool(GeneralGuiTool):
    #takes one argument. the name of the file and Name of the class
    
    toolPythonFileTemplate = """from quick.webtools.GeneralGuiTool import GeneralGuiTool\n#This is a template prototyping GUI that comes together with a corresponding web page.\n\nclass ToolTemplate(GeneralGuiTool):\n    @staticmethod\n    def getToolName():\n        return "Tool not yet in use"\n\n    @staticmethod\n    def getInputBoxNames():\n        "Returns a list of names for input boxes, implicitly also the number of input boxes to display on page. Each such box will call function getOptionsBoxK, where K is in the range of 1 to the number of boxes"\n        return ['box1','box2']\n\n    @staticmethod    \n    def getOptionsBox1():\n        "Returns a list of options to be displayed in the first options box"\n        return ['testChoice1','testChoice2','...']\n    \n    @staticmethod    \n    def getOptionsBox2(prevChoices): \n        '''Returns a list of options to be displayed in the second options box, which will be displayed after a selection is made in the first box.\n        prevChoices is a list of selections made by the web-user in the previous input boxes (that is, list containing only one element for this case)        \n        '''\n        return ['']\n    \n    \n        \n    @staticmethod    \n    def execute(choices, galaxyFn=None, username=''):\n        '''Is called when execute-button is pushed by web-user.\n        Should print output as HTML to standard out, which will be directed to a results page in Galaxy history. If getOutputFormat is anything else than HTML, the output should be written to the file with path galaxyFn.gtr\n        If needed, StaticFile can be used to get a path where additional files can be put (e.g. generated image files).\n        choices is a list of selections made by web-user in each options box.\n        '''\n        print 'Executing...'\n\n    @staticmethod\n    def validateAndReturnErrors(choices):\n        '''\n        Should validate the selected input parameters. If the parameters are not valid,\n        an error text explaining the problem should be returned. The GUI then shows this text\n        to the user (if not empty) and greys out the execute button (even if the text is empty).\n        If all parameters are valid, the method should return None, which enables the execute button.\n        '''\n        return None\n"""
    
    
    # takes argument id, name, id id == hb_xx_yy where classname == XxYy
    #Is saved under #galaxy_hb/tools/hyperbrowser/ with name xx_yy.xml
    #You also need to make a shell script for adding xml-file manually and add the other python files or do update in SVN
    toolXmlFileTemplate = """<?xml version="1.0"?>\n\n<!--\n# Copyright (C) 2009, Geir Kjetil Sandve, Sveinung Gundersen and Morten Johansen\n# This file is part of The Genomic HyperBrowser.\n#\n#    The Genomic HyperBrowser is free software: you can redistribute it and/or modify\n#    it under the terms of the GNU General Public License as published by\n#    the Free Software Foundation, either version 3 of the License, or\n#    (at your option) any later version.\n#\n#    The Genomic HyperBrowser is distributed in the hope that it will be useful,\n#    but WITHOUT ANY WARRANTY; without even the implied warranty of\n#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n#    GNU General Public License for more details.\n#\n#    You should have received a copy of the GNU General Public License\n#    along with The Genomic HyperBrowser.  If not, see <http://www.gnu.org/licenses/>.\n-->\n\n<tool tool_type="hyperbrowser_generic" id="hb_%s" name="%s"/>\n"""
    
    #path to tool_conf.developer.xml file
    
    
    #.find('</section>')
          
    @staticmethod
    def getToolName():
        return "Tool not yet in use"

    @staticmethod
    def getInputBoxNames():
        "Returns a list of names for input boxes, implicitly also the number of input boxes to display on page. Each such box will call function getOptionsBoxK, where K is in the range of 1 to the number of boxes"
        return ['Class name of new tool','Directory to save tool-script','Folder-placement for new tool']

    @staticmethod    
    def getOptionsBox1():
        "Returns a list of options to be displayed in the first options box"
        return ''
    
    @staticmethod    
    def getOptionsBox2(prevChoices):
        
        "Returns a list of options to be displayed in the first options box"
        return [v for v in os.listdir(HB_SOURCE_CODE_BASE_DIR+'/quick/webtools/') if os.path.isdir(HB_SOURCE_CODE_BASE_DIR+'/quick/webtools/'+v) and v[0]!='.']
    
    @staticmethod    
    def getOptionsBox3(prevChoices): 
        '''Returns a list of options to be displayed in the second options box, which will be displayed after a selection is made in the first box.
        prevChoices is a list of selections made by the web-user in the previous input boxes (that is, list containing only one element for this case)        
        '''
        return ['hyperbrowser', 'export_import', 'create_tracks', 'manipulate_tracks', 'nmer_analysis', 'tf_tools', 'plot_analysis', 'regulomes', 'admin_tracks_genomes','storebio_tools', 'debug_tools', 'restricted_tools', 'mcfdr_tools', 'gtrack_tools']
    
    #@staticmethod    
    #def getOptionsBox3(prevChoices):
    #    return ['']

    @staticmethod    
    def execute(choices, galaxyFn=None, username=''):
        
        
        toolName = choices[0].strip()
        xmlName = ''.join(['_'+v.lower() if v.isupper() else v for v in toolName])[1:]
        toolMenuName = ''.join([' '+v if v.isupper() else v for v in toolName])[1:]
        
        
        pythonToolFile = open(HB_SOURCE_CODE_BASE_DIR+'/quick/webtools/ToolTemplate.py','r').read().replace('ToolTemplate', toolName)
        pythonFilePath = HB_SOURCE_CODE_BASE_DIR + '/quick/webtools/'+choices[1]+'/'+toolName+'.py'
        open(pythonFilePath, 'w').write(pythonToolFile)
        
        xmlToolFilePath = HB_SOURCE_CODE_BASE_DIR + '/galaxy_hb/tools/hyperbrowser/'+xmlName+'.xml'
        toolXmlFile = open(HB_SOURCE_CODE_BASE_DIR + '/galaxy_hb/tools/hyperbrowser/genericTool_2.xml','r').read().replace('generic_2', xmlName).replace('Generic tool 2', toolMenuName)
        open(xmlToolFilePath, 'w').write(toolXmlFile)
        
        toolConfXmlPath = HB_SOURCE_CODE_BASE_DIR+'/galaxy_hb/custom/tool_conf.developer.xml'
        toolConfXml = open(toolConfXmlPath, 'r').read()
        
        toolPlacement = choices[2].strip()
        
        ToolConfXmlIndx1 = toolConfXml.find('id="%s">' % toolPlacement)
        ToolConfXmlInsertIndex = ToolConfXmlIndx1 + toolConfXml[toolConfXml.find('id="%s">' % toolPlacement):].find('</section>')
        resultToolConfXml = toolConfXml[:ToolConfXmlInsertIndex]+ ('          <tool file="hyperbrowser/%s.xml" />\n' % xmlName) +toolConfXml[ToolConfXmlInsertIndex:]
        open(toolConfXmlPath, 'w').write(resultToolConfXml)
        
        generalGuiToolFactoryPath = HB_SOURCE_CODE_BASE_DIR+'/quick/webtools/GeneralGuiToolsFactory.py'
        generalGuiToolFactory = open(generalGuiToolFactoryPath, 'r').read()
        replacementStr = 'from quick.webtools.%s import %s \n\nclass GeneralGuiToolsFactory:' % (choices[1]+'.'+toolName,toolName)
        generalGuiToolFactoryInsertIndex = generalGuiToolFactory.find('else:')
        resultGeneralGuiToolFactory = generalGuiToolFactory[:generalGuiToolFactoryInsertIndex]+ \
            ("elif toolId == 'hb_%s':\n            return %s()\n        " % (xmlName, toolName)) +generalGuiToolFactory[generalGuiToolFactoryInsertIndex:]
        open(generalGuiToolFactoryPath, 'w').write(resultGeneralGuiToolFactory.replace('\nclass GeneralGuiToolsFactory:', replacementStr))
        
        # install new/changed files
        os.chdir(HB_SOURCE_CODE_BASE_DIR)
        os.system('python setup/Install.py')

        # signal that restart of galaxy is required
        print "Restart in progress..."
        #open(GALAXY_BASE_DIR + '/NEED_RESTART', 'w').close();
        
        

    @staticmethod
    def validateAndReturnErrors(choices):
        if os.path.exists(HB_SOURCE_CODE_BASE_DIR + '/quick/webtools/'+choices[0].strip()+'.py'):
            return 'Tool with name "%s" already exists. Please rename your tool' % choices[0].strip()
        xmlName = ''.join(['_'+v.lower() if v.isupper() else v for v in choices[0].strip()])[1:]
        if os.path.exists(HB_SOURCE_CODE_BASE_DIR + '/galaxy_hb/tools/hyperbrowser/ '+xmlName+'.xml'):
            return 'Xml file for Tool with name "%s" already exists. Please rename your tool or delete xml file' % choices[0].strip()
        '''
        Should validate the selected input parameters. If the parameters are not valid,
        an error text explaining the problem should be returned. The GUI then shows this text
        to the user (if not empty) and greys out the execute button (even if the text is empty).
        If all parameters are valid, the method should return None, which enables the execute button.
        '''
        return None