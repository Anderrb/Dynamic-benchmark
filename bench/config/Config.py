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

from config.LocalOSConfig import *
from config.AutoConfig import *

#
# Version information
#

HB_VERSION = 'v1.5.2'
GALAXY_VERSION = 'fa0b5c68d097'
# '26920e20157f'

#
# Functionality settings
#

USE_MEMORY_MEMOIZATION = True
LOAD_DISK_MEMOIZATION = False
STORE_DISK_MEMOIZATION = False
PRINT_PROGRESS = True
#Currently not used. See CompBinManager:
ALLOW_COMP_BIN_SPLITTING = False

#
# Optimization and limits
#

COMP_BIN_SIZE = 100000
FILE_READ_BUFFER_SIZE = 1024 * 1024
MEMMAP_BIN_SIZE = 1 * FILE_READ_BUFFER_SIZE
MAX_NUM_USER_BINS = 330000
MAX_LOCAL_RESULTS_IN_TABLE = 100000
OUTPUT_PRECISION = 4
TEST_DEBUG = False
USE_PARALLEL = False
BATCH_COL_SEPARATOR = '|'
MULTIPLE_EXTRA_TRACKS_SEPARATOR = '&'
MAX_CONCAT_LEN_FOR_OVERLAPPING_ELS = 20

#
# Debug options
#

#VERBOSE = False
#PASS_ON_VALIDSTAT_EXCEPTIONS = False
#PASS_ON_COMPUTE_EXCEPTIONS = False
#PASS_ON_BATCH_EXCEPTIONS = True
USE_PROFILING = False
#TRACE_STAT = {'computeStep': True, 'compute': True, '_compute': True, '_combineResults': True, '_createChildren': True, '__init__': True, '_afterComputeCleanup' : True, '_prepareForNewIteration' : True, '_setNotMemoizable' : True, '_updateInMemoDict' : True, 'printRegions':True, 'printTrackNames':True}
#TRACE_STAT = {'computeStep': False, 'compute': False, '_compute': False, '_combineResults': False, '_createChildren': False, '__init__': True, '_afterComputeCleanup' : True, '_prepareForNewIteration' : True, '_setNotMemoizable' : True, '_updateInMemoDict' : True, 'printRegions':True, 'printTrackNames':True}
TRACE_STAT = {'computeStep': False, 'compute': False, '_compute': False, '_combineResults': False, '_createChildren': False, '__init__': False, '_afterComputeCleanup' : False, '_prepareForNewIteration' : False, '_setNotMemoizable' : False, '_updateInMemoDict' : False, 'printRegions':True, 'printTrackNames':True}

class DebugConfig:
    VERBOSE = False
    PASS_ON_VALIDSTAT_EXCEPTIONS = False
    PASS_ON_COMPUTE_EXCEPTIONS = False
    PASS_ON_BATCH_EXCEPTIONS = False
    PASS_ON_NONERESULT_EXCEPTIONS = False
#
# To be removed
#

DEFAULT_GENOME = 'hg18'
