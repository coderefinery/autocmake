import os
import sys
import subprocess
import shlex
import shutil
import sys
import time
import datetime
import pytest

HERE = os.path.abspath(os.path.dirname(__file__))

skip_on_osx = pytest.mark.skipif('sys.platform == "darwin"', reason="not working on osx")
skip_on_linux = pytest.mark.skipif('sys.platform == "linux2"', reason="not working on linux")
skip_always = pytest.mark.skipif('1 == 1', reason="tests are broken")


def exe(command):
    """
    Executes command and returns string representations of stdout and stderr captured from the console.
    When universal_newlines=True stdout and stderr are opened in text mode.
    Otherwise, they are opened in binary mode. In that case captured stdout and stderr
    are not strings and Python 3 throws type error when compared against strings later in tests.
    Note:
    This feature is only available if Python is built with universal newline support (the default).
    Also, the newlines attribute of the file objects stdout, stdin and stderr are not updated by the
    communicate() method.
    See https://docs.python.org/2/library/subprocess.html
    """
    stdout, stderr = subprocess.Popen(shlex.split(command),
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      universal_newlines=True).communicate()

    if stderr:
        sys.stderr.write(stdout)
        sys.stderr.write(stderr)

    return stdout, stderr


def configure_build_and_exe(name, setup_command, launcher=None):

    stamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')

    os.chdir(os.path.join(HERE, name, 'cmake'))
    shutil.copy(os.path.join('..', '..', '..', 'update.py'), 'update.py')

    if os.path.exists('autocmake'):
        shutil.rmtree('autocmake')
    shutil.copytree(os.path.join('..', '..', '..', 'autocmake'), 'autocmake')

    stdout, stderr = exe('python update.py ..')
    os.chdir(os.path.join(HERE, name))

    make_command = 'make'
    binary = './bin/example'
    if sys.platform == 'win32':
        setup_command += ' --generator="MinGW Makefiles"'
        make_command = 'mingw32-make'
        binary = 'bin\\\example.exe'

    if launcher:
        binary = '%s %s' % (launcher, binary)

    setup_command += ' build-%s' % stamp

    stdout, stderr = exe(setup_command)
    assert stderr == ''

    os.chdir(os.path.join(HERE, name, 'build-%s' % stamp))

    stdout, stderr = exe(make_command)
    # we do not check for empty stderr due to warnings flushed to stderr

    stdout, stderr = exe(binary)
    assert stderr == ''

    assert 'PASSED' in stdout


def test_fc():
    configure_build_and_exe('fc', 'python setup --fc=gfortran')


def test_fc_blas():
    configure_build_and_exe('fc_blas', 'python setup --fc=gfortran --blas')


@skip_on_osx
def test_fc_openblas():
    configure_build_and_exe('fc_blas', 'python setup --fc=gfortran --openblas')
