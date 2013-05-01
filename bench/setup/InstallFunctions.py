import os
import sys
import subprocess

from gold.util.CustomExceptions import ExecuteError

def _handleError(msg, printError, onError):
    if printError:
        print 'FAILED: ' + msg
    if onError == 'exit':
        sys.exit(1)
    elif onError == 'exception':
        raise ExecuteError(msg)

def _executeCmd(cmd, fn=None, scriptType='', cwd=None, pipe=False, printError=True, onError='exit'):
    onError = onError.lower()
    onError.lower() in ['exit', 'exception', 'nothing']
    p = subprocess.Popen(args=cmd, shell = True, cwd = cwd, \
                         stdout = subprocess.PIPE if pipe else None, stderr = subprocess.PIPE if pipe else None)
    if pipe:
        r = p.communicate()
        if r[1]:
            msg = 'Not able to execute %sscript: %s. Error: %s' \
                  % (scriptType + ' ' if scriptType else '', fn if fn else cmd, r[1])
            _handleError(msg, printError, onError)
        return r[0]
    else:
        r = p.wait()
        if r != 0:
            msg = 'Not able to execute %sscript: %s (Return code: %d)' % (scriptType + ' ' if scriptType else '', fn if fn else cmd, r)
            _handleError(msg, printError, onError)
        return r

def executePythonFile(pyFn, args='', cwd=None, printError=True, onError='exit', setPythonPath=False):
    from config.Config import GALAXY_LIB_PATH
    
    origPyFn = pyFn
    if not cwd:
        cwd = os.path.dirname(pyFn)
        pyFn = os.path.basename(pyFn)
#    cmd = ' '.join([sys.executable, PYTHON_EXECUTE_OPTIONS, pyFn, args])
    cmd = ' '.join([sys.executable, pyFn, args])
    if setPythonPath:
        from config.Config import HB_SOURCE_CODE_BASE_DIR, GALAXY_BASE_DIR, HB_PYTHONPATH
        cmd = 'export PYTHONPATH="%s:%s:%s:%s"; ' % \
              (HB_SOURCE_CODE_BASE_DIR, GALAXY_LIB_PATH, GALAXY_BASE_DIR + os.sep + 'eggs', HB_PYTHONPATH) + cmd
    _executeCmd(cmd, origPyFn, 'python', cwd=cwd, printError=printError, onError=onError)

def executeShellFile(shFn, args='', cwd=None, printError=True, onError='exit'):
    origShFn = shFn
    if not cwd:
        cwd = os.path.dirname(shFn)
        shFn = os.path.basename(shFn)
    _executeCmd( ' '.join(['sh', shFn]) + ' '.join(args), \
                origShFn, 'shell', cwd=cwd, printError=printError, onError=onError)
    
def executeShellCmd(cmd, args='', pipe=True, printError=True, onError='exit'):
    return _executeCmd(cmd, None, 'shell', pipe=pipe, printError=printError, onError=onError)
