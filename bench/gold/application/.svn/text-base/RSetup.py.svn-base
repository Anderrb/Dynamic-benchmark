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

try:
    try:
        from galaxy import eggs
        eggs.pkg_resources.require('rpy2')
    except:
        pass
    
    #from rpy import r
    from quick.application.parallel.Worker import IS_WORKER
    import rpy2.robjects as robjects
        
    import rpy2.rinterface as rinterface
    from rpy2.robjects import r
    import rpy2.rpy_classic
    rpy2.rpy_classic.set_default_mode(rpy2.rpy_classic.NO_CONVERSION)
    from rpy2.rpy_classic import r as rpy1
 
    #import rpy2.robjects.numpy2ri #This needs to be changed when upgrading to rpy2 2.2 or higher. 
    #                              #Just uncomment the three lines below and remove this line.
    #                              
    import rpy2.robjects.numpy2ri as rpyn
    robjects.conversion.py2ri = rpyn.numpy2ri
    robjects.conversion.ri2numpy = rpyn.ri2numpy
    rpy2.robjects.numpy2ri.activate()

    #    r("install.packages('maptree', repos='http://cran.r-project.org')")
        #set_default_mode(BASIC_CONVERSION)
    
        
        
    def custom_py2ri(obj):
       res = replaceNone(obj)
       
       return original_conversion(res)
     
    def replaceNone(obj):
       if isinstance(obj, list):
           for x in obj:
               x = replaceNone(x)
       
       if obj is None:
           obj = robjects.NA_Logical
           
       return obj
     
    #In case the conversion in use now is not the default, save it so that custom_py2ri can
    #use it. This happens if for example numpy conversion is turned on
    original_conversion = robjects.conversion.py2ri 
    robjects.conversion.py2ri = custom_py2ri
     
    def custom_ri2py(obj):
       res = robjects.default_ri2py(obj)
       
       if isinstance(res, robjects.Vector) and (len(res) == 1):
           res = super(robjects.vectors.Vector, res).__getitem__(0)
           
           if isinstance(res, rinterface.Sexp):
               res = robjects.default_ri2py(res)
               
       return res
         
    robjects.conversion.ri2py = custom_ri2py

except Exception, e:
    print "Failed importing rpy2. Error: ", e
    #raise e
    #from rpy2.robjects import r
    #from rpy2.rpy_classic import r #, BASIC_CONVERSION, NO_CONVERSION, set_default_mode
    #set_default_mode(BASIC_CONVERSION)
    #set_default_mode(NO_CONVERSION)
    
def getRVersion():
    #verDict={"major":"2", "minor":"13.2"}
    #verDict = rpy1('version')
    verDict = r('version')
    try:
        return '%s.%s' % (verDict.rx2('major')[0], verDict.rx2('minor')[0])
    except:
        return '%s.%s' % (verDict[verDict.names.index('major')], verDict[verDict.names.index('minor')])

    
#R_VERSION = getRVersion()