HB_SOURCE_CODE_BASE_DIR = '/usit/invitro/data/hyperbrowser/hb_core_bench'
GALAXY_BASE_DIR = '/usit/invitro/data/galaxy/galaxy_bench'

IS_EXPERIMENTAL_INSTALLATION = True

RESTRICTED_USERS = 'sveinugu2@gmail.com, anderrb@ifi.uio.no, geirkjetil@gmail.com, fredrik@nbmedia.no'

PYTHON_EXECUTE_OPTIONS = ''

#
# Environment variables
#

HB_PYTHONPATH = '.:/site/VERSIONS/python-2.7.gcc45/lib:/usit/invitro/data/common_software/lib/python2.7/site-packages:/usit/invitro/data/common_software/bin/Komodo-PythonRemoteDebugging-4.3.2-17463-linux-x86'
#HB_RHOME = '/cluster/software/VERSIONS/R-2.15.1.shlib/lib64/R'
HB_RHOME = '/site/VERSIONS/R-2.13.2.shlib/lib64/R'
HB_R_LIBS = ''
HB_EXTRA_R_LIBRARIES = ''

HB_XVFB_DISPLAY = ":20.0"

#
# Web customization
#

GALAXY_URL = 'http://hyperbrowser.uio.no'

HEADER_TITLE = 'The Genomic HyperBrowser (benchmarking version)'
HEADER_SMALL_LOGO_IMAGE = 'HB_logo_title_small.png'

WELCOME_NOTICE_HTML = '<div class="noticebox"><b>Notice</b> <p><i>This is an unstable version of The Genomic HyperBrowser for a master project on benchmarking and is not suited for public use. If you are a user, you should instead use the stable <a href="http://hyperbrowser.uio.no" target="main">main version of the HyperBrowser</a>. The user and history database is not the same between the different versions.</i></p></div>'
WELCOME_LOGO_IMAGE = 'HB_logo.png'
WELCOME_TITLE_IMAGE = 'HB_title.png'

GALAXY_HTML_META_TAGS = ''
GOOGLE_ANALYTICS_WEB_PROPERTY_ID = 'UA-26271415-1'

GALAXY_COLOR_DEFINITION_FILE = 'HB_colors.ini'
GALAXY_COMPILE_COLORS = True

#END_DEFAULT

#
# External paths
#

EXT_NONSTANDARD_DATA_PATH = '/usit/invitro/hyperbrowser/collectedTracks'
EXT_ORIG_DATA_PATH = '/usit/invitro/hyperbrowser/standardizedTracks'
EXT_PARSING_ERROR_DATA_PATH = '/usit/invitro/hyperbrowser/parsingErrorTracks'
EXT_PROCESSED_DATA_PATH = '/usit/invitro/hyperbrowser/preProcessed'
EXT_MEMOIZED_DATA_PATH = '/usit/invitro/fast/hyperbrowser/memoCPickles'

EXT_DATA_FILES_PATH = '/usit/invitro/hyperbrowser/data'
EXT_UPLOAD_FILES_PATH = '/usit/invitro/work/hyperbrowser/nosync/nobackup/upload'
EXT_STATIC_FILES_PATH = '/usit/invitro/hyperbrowser/staticFiles/'
EXT_NMER_CHAIN_DATA_PATH = '/usit/invitro/hyperbrowser/nmerChains'
EXT_MAPS_PATH = '/usit/invitro/work/hyperbrowser/nosync/maps'
EXT_LOG_PATH = '/usit/invitro/work/hyperbrowser/nosync/logs/bench'
EXT_RESULTS_PATH = '/usit/invitro/hyperbrowser/results/bench'
EXT_VIDEOS_PATH = '/usit/invitro/hyperbrowser/videos'
EXT_TMP_PATH = '/usit/invitro/work/tmp'

#
# Galaxy setup
#

URL_PREFIX = '/bench'

GALAXY_JOB_RUNNER_PORT = '59111'
GALAXY_JOB_RUNNER_THREADPOOL_WORKERS = '5'
GALAXY_WEB_SERVER_PORT = '58110'
GALAXY_WEB_SERVER_THREADPOOL_WORKERS = '10'
GALAXY_ADDITIONAL_WEB_SERVER_COUNT = '1'
GALAXY_TRANSFER_MANAGER_PORT = '57110'
GALAXY_LOCAL_JOB_QUEUE_WORKERS = '8'

GALAXY_DATABASE_CONNECTION = 'mysql://galaxy_bench:yxalag2@localhost/galaxy_bench?unix_socket=/var/lib/mysql/mysql.sock'
GALAXY_SMTP_SERVER = 'smtp.uio.no'
GALAXY_MAILING_LIST_ADDR = 'hyperbrowser-info@usit.uio.no'
GALAXY_BUGS_EMAIL = 'hyperbrowser-bugs@usit.uio.no'
GALAXY_REQUESTS_EMAIL_URL = 'mailto:hyperbrowser-requests@usit.uio.no'
GALAXY_SYMPA_MANAGEMENT_ADDR = 'sympa@usit.uio.no'

GALAXY_DEBUG = True
GALAXY_ID_SECRET = 'Dksdj!j541dlslkfj546&$44dsdfsaDDDkper'
GALAXY_ADMIN_USERS = 'sveinugu2@gmail.com,anderrb@ifi.uio.no'

GALAXY_ADDITIONAL_SETTINGS = '''
#Write any additional galaxy settings here (will appear under the [app:main] heading):
database_engine_option_strategy = threadlocal
allow_user_deletion = True
enable_pages = True
set_metadata_externally = True
enable_tracks = True
'''

#
# Parallel setup
#

CLUSTER_ACCOUNTNAME = "ghbrowse"
CLUSTER_TEMP_PATH="/xanadu/project/rrresearch/jonathal/titanRuns"
CLUSTER_SOURCE_CODE_DIRECTORY = "/xanadu/project/rrresearch/new_hb_titan_mptesting/mptesting"
ONLY_USE_ENTIRE_CLUSTER_NODES = False
CLUSTER_CORES_PER_NODE = 8
SBATCH_PATH = "/site/bin/sbatch"
CLUSTER_MEMORY_PER_CORE_IN_MB=2048
DEFAULT_WALLCLOCK_LIMIT_IN_SECONDS=3600
DEFAULT_NUMBER_OF_REMOTE_WORKERS = 8

PP_NUMBER_OF_LOCAL_WORKERS = 2
PP_PASSPHRASE = "54fdsiu5e6&@#sdO"
PP_PORT=56110
PP_MANAGER_PORT=55110

#
# Debug code
#

#from dbgp.client import brkOnExcept
#brkOnExcept(host='localhost', port=9000, idekey='galaxy')
#from dbgp.client import brk
#brk(host='localhost', port=9000, idekey='galaxy')
