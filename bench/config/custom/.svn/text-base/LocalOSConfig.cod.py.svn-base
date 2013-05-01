HB_SOURCE_CODE_BASE_DIR = '/usit/invitro/data/hyperbrowser/hb_core_cod'
GALAXY_BASE_DIR = '/usit/invitro/data/galaxy/galaxy_cod'

IS_EXPERIMENTAL_INSTALLATION = True

RESTRICTED_USERS = 'morj@rr-research.no, sveinugu@gmail.com, geirkjetil@gmail.com, t.b.rounge@bio.uio.no, lex.nederbragt@bio.uio.no, karin.lagesen@bio.uio.no, martin.malmstrom@bio.uio.no, trengere@gmail.com'

PYTHON_EXECUTE_OPTIONS = ''

#
# Environment variables
#

HB_PYTHONPATH = '.:/site/VERSIONS/python-2.7.gcc45/lib:/usit/invitro/data/common_software/lib/python2.7/site-packages:/usit/invitro/data/common_software/bin/Komodo-PythonRemoteDebugging-4.3.2-17463-linux-x86'
#HB_RHOME = '/cluster/software/VERSIONS/R-2.15.1.shlib/lib64/R'
HB_RHOME = '/site/VERSIONS/R-2.13.2.shlib/lib64/R'
HB_R_LIBS = ''
HB_EXTRA_R_LIBRARIES = ''

HB_XVFB_DISPLAY = ":14.0"

#
# Web customization
#

GALAXY_URL = 'http://hyperbrowser.uio.no'

HEADER_TITLE = 'The Genomic HyperBrowser (cod version)'
HEADER_SMALL_LOGO_IMAGE = 'HB_logo_title_small.png'

WELCOME_NOTICE_HTML = '<div class="noticebox"><b>Notice</b> <p><i>This is the cod version of The Genomic Hyperbrowser. The user and history database is not the same as the one used in the stable version (hyperbrowser.uio.no/hb).</i></p></div>'
WELCOME_LOGO_IMAGE = 'custom/HB_logo_cod_same_line.png'

GALAXY_HTML_META_TAGS = ''
GOOGLE_ANALYTICS_WEB_PROPERTY_ID = 'UA-26271029-1'

GALAXY_COLOR_DEFINITION_FILE = 'HB_colors_cod.ini'
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
EXT_LOG_PATH = '/usit/invitro/work/hyperbrowser/nosync/logs/cod'
EXT_RESULTS_PATH = '/usit/invitro/hyperbrowser/results/cod'
EXT_VIDEOS_PATH = '/usit/invitro/hyperbrowser/videos'
EXT_TMP_PATH = '/usit/invitro/work/tmp'

#
# Galaxy setup
#

URL_PREFIX = '/cod'

GALAXY_JOB_RUNNER_PORT = '59040'
GALAXY_JOB_RUNNER_THREADPOOL_WORKERS = '5'
GALAXY_WEB_SERVER_PORT = '58040'
GALAXY_WEB_SERVER_THREADPOOL_WORKERS = '10'
GALAXY_ADDITIONAL_WEB_SERVER_COUNT = '1'
GALAXY_TRANSFER_MANAGER_PORT = '57040'
GALAXY_LOCAL_JOB_QUEUE_WORKERS = '4'

GALAXY_DATABASE_CONNECTION = 'mysql://galaxy_cod:yxalag2@localhost/galaxy_cod?unix_socket=/var/lib/mysql/mysql.sock'
GALAXY_SMTP_SERVER = 'smtp.uio.no'
GALAXY_MAILING_LIST_ADDR = 'hyperbrowser-info@usit.uio.no'
GALAXY_BUGS_EMAIL = 'hyperbrowser-bugs@usit.uio.no'
GALAXY_REQUESTS_EMAIL_URL = 'mailto:hyperbrowser-requests@usit.uio.no'
GALAXY_SYMPA_MANAGEMENT_ADDR = 'sympa@usit.uio.no'

GALAXY_DEBUG = True
GALAXY_ID_SECRET = 'sdjf87sdfiwr8724y234rgf78u23fffv'
GALAXY_ADMIN_USERS = 'morj@rr-research.no,sveinugu@gmail.com,geirkjetil@gmail.com,trengere@gmail.com'

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
PP_PASSPHRASE = "ASJKhds^g2376f"
PP_PORT=56040
PP_MANAGER_PORT=55040

#
# Debug code
#

#from dbgp.client import brkOnExcept
#brkOnExcept(host='localhost', port=9000, idekey='galaxy')
#from dbgp.client import brk
#brk(host='localhost', port=9000, idekey='galaxy')
