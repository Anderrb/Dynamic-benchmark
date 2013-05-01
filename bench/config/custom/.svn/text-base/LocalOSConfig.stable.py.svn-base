HB_SOURCE_CODE_BASE_DIR = '/usit/invitro/data/hyperbrowser/hb_core_stable'
GALAXY_BASE_DIR = '/usit/invitro/data/galaxy/galaxy_stable'

IS_EXPERIMENTAL_INSTALLATION = False

RESTRICTED_USERS = 'geirkjetil@gmail.com, morj@rr-research.no, ehovig@ifi.uio.no, morj@medisin.uio.no, halfdan.rydbeck@rr-research.no, lundandersen@gmail.com, sveinugu@gmail.com, hrydbeck@gmail.com, Marit.Holden@nr.no, tlavelle@rr-research.no, vegardny@radium.uio.no, kristian@bioinfo.hr, trevor.clancy@rr-research.no, stale.nygard@medisin.uio.no, hiepln@ifi.uio.no, eivindgl@student.matnat.uio.no, jonaspau@ifi.uio.no, finn.drablos@ntnu.no, oyvind.overgaard@gmail.com, trengere@gmail.com, sigve.nakken@medisin.uio.no, waloeen@gmail.com'

PYTHON_EXECUTE_OPTIONS = ''

#
# Environment variables
#

#HB_PYTHONPATH = '.:/site/VERSIONS/python-2.7.gcc45/lib:/usit/invitro/data/common_software/lib/python2.7/site-packages:/usit/invitro/data/common_software/bin/Komodo-PythonRemoteDebugging-4.3.2-17463-linux-x86'
HB_PYTHONPATH = '.:/site/VERSIONS/python-2.7.gcc45/lib:/usit/invitro/data/common_software/lib/python2.7/site-packages'
#HB_RHOME = '/cluster/software/VERSIONS/R-2.15.1.shlib/lib64/R'
HB_RHOME = '/site/VERSIONS/R-2.13.2.shlib/lib64/R'
HB_R_LIBS = ''
HB_EXTRA_R_LIBRARIES = ''

HB_XVFB_DISPLAY = ":10.0"

#
# Web customization
#

GALAXY_URL = 'http://hyperbrowser.uio.no'

HEADER_TITLE = 'The Genomic HyperBrowser'
HEADER_SMALL_LOGO_IMAGE = 'HB_logo_title_small.png'

WELCOME_NOTICE_HTML = ''
WELCOME_LOGO_IMAGE = 'HB_logo_same_line.png'

GALAXY_HTML_META_TAGS = '<meta name="google-site-verification" content="pC4JbkPDJPTUV-8YZ-KAGMSqTOc3OqVrP-ECovoWklE" />'
GOOGLE_ANALYTICS_WEB_PROPERTY_ID = 'UA-26271401-1'

GALAXY_COLOR_DEFINITION_FILE = 'HB_colors.ini'
GALAXY_COMPILE_COLORS = False

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
EXT_LOG_PATH = '/usit/invitro/work/hyperbrowser/nosync/logs/stable'
EXT_RESULTS_PATH = '/usit/invitro/hyperbrowser/results/stable'
EXT_VIDEOS_PATH = '/usit/invitro/hyperbrowser/videos'
EXT_TMP_PATH = '/usit/invitro/work/tmp'

#
# Galaxy setup
#

URL_PREFIX = '/hb'

GALAXY_JOB_RUNNER_PORT = '59081'
GALAXY_JOB_RUNNER_THREADPOOL_WORKERS = '60'
GALAXY_WEB_SERVER_PORT = '58080'
GALAXY_WEB_SERVER_THREADPOOL_WORKERS = '10'
GALAXY_ADDITIONAL_WEB_SERVER_COUNT = '2'
GALAXY_TRANSFER_MANAGER_PORT = '57080'
GALAXY_LOCAL_JOB_QUEUE_WORKERS = '16'

GALAXY_DATABASE_CONNECTION = 'mysql://galaxy_stable:yxalag2@localhost/galaxy_stable?unix_socket=/var/lib/mysql/mysql.sock'
GALAXY_SMTP_SERVER = 'smtp.uio.no'
GALAXY_MAILING_LIST_ADDR = 'hyperbrowser-info@usit.uio.no'
GALAXY_BUGS_EMAIL = 'hyperbrowser-bugs@usit.uio.no'
GALAXY_REQUESTS_EMAIL_URL = 'mailto:hyperbrowser-requests@usit.uio.no'
GALAXY_SYMPA_MANAGEMENT_ADDR = 'sympa@usit.uio.no'

GALAXY_DEBUG = True
GALAXY_ID_SECRET = 'sdf978364834jfhhuds6f8374yrw'
GALAXY_ADMIN_USERS = 'morj@rr-research.no,sveinugu@gmail.com,geirkjetil@gmail.com,harad@ifi.uio.no'

GALAXY_ADDITIONAL_SETTINGS = '''
#Write any additional galaxy settings here (will appear under the [app:main] heading):
database_engine_option_strategy = threadlocal
allow_user_deletion = True
enable_pages = True
set_metadata_externally = True
enable_tracks = True
ftp_upload_dir = %s
ftp_upload_site = "Please_ignore_this"
enable_quotas = True
''' % EXT_UPLOAD_FILES_PATH

#
# StoreBioInfo setup
#

STOREBIOINFO_USER = 'kaitre'
STOREBIOINFO_PASSWD = 'katrno'

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
PP_PASSPHRASE = "dhdsI#&477kHsgy"
PP_PORT=56080
PP_MANAGER_PORT=55080

#
# Debug code
#

#from dbgp.client import brkOnExcept
#brkOnExcept(host='localhost', port=9000, idekey='galaxy')
#from dbgp.client import brk
#brk(host='localhost', port=9000, idekey='galaxy')
