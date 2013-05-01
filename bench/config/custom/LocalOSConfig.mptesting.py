HB_SOURCE_CODE_BASE_DIR = '/xanadu/home/jonathal/my_hb'
GALAXY_BASE_DIR = '/usit/invitro/data/galaxy/galaxy_mptesting'

IS_EXPERIMENTAL_INSTALLATION = True

RESTRICTED_USERS = 'geirkjetil@gmail.com, morj@rr-research.no, ehovig@ifi.uio.no, morj@medisin.uio.no, halfdan.rydbeck@rr-research.no, lundandersen@gmail.com, sveinugu@gmail.com, hrydbeck@gmail.com, Marit.Holden@nr.no, tlavelle@rr-research.no, vegardny@radium.uio.no, kristian@bioinfo.hr, trevor.clancy@rr-research.no, stale.nygard@medisin.uio.no, hiepln@ifi.uio.no, eivindgl@student.matnat.uio.no, jonaspau@ifi.uio.no, finn.drablos@ntnu.no, oyvind.overgaard@gmail.com, trengere@gmail.com, jonathal@ifi.uio.no'

PYTHON_EXECUTE_OPTIONS = ''

#
# Environment variables
#

HB_PYTHONPATH = '$PYTHONPATH:/projects/rrresearch/common_software/lib/python2.7/site-packages'
HB_RHOME = '/xanadu/site/common/VERSIONS/R-2.10.1/lib64/R'
HB_R_LIBS = '/projects/rrresearch/common_software/lib/R-2.10.1/library'
HB_XVFB_DISPLAY = ":12.0"

#
# Web customization
#

GALAXY_URL = 'http://hyperbrowser.uio.no'

HEADER_TITLE = 'The Genomic HyperBrowser (developer version)'
HEADER_SMALL_LOGO_IMAGE = 'HB_logo_title_small.png'

WELCOME_NOTICE_HTML = '<b>Notice</b> <p><i>This is the mptesting version of The Genomic Hyperbrowser. The user and history database is not the same as the one used in the stable version (hyperbrowser.uio.no/hb).</i></p>'
WELCOME_LOGO_IMAGE = 'HB_logo.png'
WELCOME_TITLE_IMAGE = 'HB_title.png'

GALAXY_HTML_META_TAGS = ''
GOOGLE_ANALYTICS_WEB_PROPERTY_ID = 'UA-26271415-1'

GALAXY_COLOR_DEFINITION_FILE = 'HB_colors.ini'
GALAXY_COMPILE_COLORS = False

#END_DEFAULT

#
# External paths
#

EXT_NONSTANDARD_DATA_PATH = '/norstore_osl/hyperbrowser/nosync/collectedTracks'
EXT_ORIG_DATA_PATH = '/usit/invitro/hyperbrowser/standardizedTracks'
EXT_PARSING_ERROR_DATA_PATH = '/usit/invitro/hyperbrowser/parsingErrorTracks'
EXT_PROCESSED_DATA_PATH = '/usit/invitro/hyperbrowser/preProcessed'
EXT_MEMOIZED_DATA_PATH = '/usit/invitro/fast/hyperbrowser/memoCPickles'

EXT_DATA_FILES_PATH = '/usit/invitro/hyperbrowser/data'
EXT_NMER_CHAIN_DATA_PATH = '/norstore_osl/hyperbrowser/nosync/nmerChains'
#EXT_NMER_CHAIN_DATA_PATH = '/usit/invitro/fast/hyperbrowser/NmerChains'
EXT_MAPS_PATH = '/usit/invitro/work/hyperbrowser/nosync/maps'
EXT_LOG_PATH = '/usit/invitro/work/hyperbrowser/nosync/logs/mptesting'
EXT_RESULTS_PATH = '/usit/invitro/hyperbrowser/results/mptesting'
EXT_VIDEOS_PATH = '/usit/invitro/hyperbrowser/videos'
EXT_TMP_PATH = '/usit/invitro/work/tmp'

#
# Galaxy setup
#

URL_PREFIX = '/mptesting'

GALAXY_JOB_RUNNER_PORT = '59050'
GALAXY_JOB_RUNNER_THREADPOOL_WORKERS = '5'
GALAXY_WEB_SERVER_PORT = '58050'
GALAXY_WEB_SERVER_THREADPOOL_WORKERS = '10'
GALAXY_ADDITIONAL_WEB_SERVER_COUNT = '1'
GALAXY_TRANSFER_MANAGER_PORT = '57050'
GALAXY_LOCAL_JOB_QUEUE_WORKERS = '4'

GALAXY_DATABASE_CONNECTION = 'mysql://galaxy_mptesting:yxalag2@localhost/galaxy_mptesting?unix_socket=/var/lib/mysql/mysql.sock'
GALAXY_SMTP_SERVER = 'smtp.uio.no'
GALAXY_MAILING_LIST_ADDR = 'hyperbrowser-info@usit.uio.no'
GALAXY_BUGS_EMAIL = 'hyperbrowser-bugs@usit.uio.no'
GALAXY_REQUESTS_EMAIL_URL = 'mailto:hyperbrowser-requests@usit.uio.no'
GALAXY_SYMPA_MANAGEMENT_ADDR = 'sympa@usit.uio.no'

GALAXY_DEBUG = True
GALAXY_ID_SECRET = '5723645uy23462tuawetr823u6gj23'
GALAXY_ADMIN_USERS = 'morj@rr-research.no,sveinugu@gmail.com,geirkjetil@gmail.com'

GALAXY_ADDITIONAL_SETTINGS = '''
#Write any additional galaxy settings here (will appear under the [app:main] heading):
database_engine_option_strategy = threadlocal
allow_user_deletion = True
enable_pages = True
set_metadata_externally = True
'''

#
# Debug code
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

PP_NUMBER_OF_LOCAL_WORKERS = 4
PP_PASSPHRASE = "Tu8CC!cfWwS"
PP_PORT=56050
PP_MANAGER_PORT=55050
#from dbgp.client import brkOnExcept
#brkOnExcept(host='localhost', port=9000, idekey='galaxy')
#from dbgp.client import brk
#brk(host='localhost', port=9000, idekey='galaxy')