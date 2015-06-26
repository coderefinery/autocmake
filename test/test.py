import os
import sys
import subprocess

HERE = os.path.abspath(os.path.dirname(__file__))

#-------------------------------------------------------------------------------

def exe(command):
    stdout, stderr = subprocess.Popen(command.split(),
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE).communicate()
    return stdout, stderr

#-------------------------------------------------------------------------------

def test_cxx():
    os.chdir(os.path.join(HERE, 'cxx', 'cmake'))
    if  sys.platform == 'win32':
	    stdout, stderr = exe('python -m wget https://github.com/miroi/autocmake/raw/master/update.py')
    else:
        stdout, stderr = exe('wget https://github.com/miroi/autocmake/raw/master/update.py')
    stdout, stderr = exe('python update.py --self')
    stdout, stderr = exe('python update.py ..')
    os.chdir(os.path.join(HERE, 'cxx'))
    if  sys.platform == 'win32':
        stdout, stderr = exe('python setup.py --cxx=g++ --generator="MinGW Makefiles"')
    else:
        stdout, stderr = exe('python setup.py --cxx=g++')
    os.chdir(os.path.join(HERE, 'cxx', 'build'))
    if  sys.platform == 'win32':
        stdout, stderr = exe('mingw32-make')
        stdout, stderr = exe('bin\example.exe')
    else:
        stdout, stderr = exe('make')
        stdout, stderr = exe('./bin/example')
    assert 'Hello World!' in stdout

#-------------------------------------------------------------------------------

def test_fc():
    os.chdir(os.path.join(HERE, 'fc', 'cmake'))
    if  sys.platform == 'win32':
	    stdout, stderr = exe('python -m wget https://github.com/miroi/autocmake/raw/master/update.py')
    else:
        stdout, stderr = exe('wget https://github.com/miroi/autocmake/raw/master/update.py')
    stdout, stderr = exe('python update.py --self')
    stdout, stderr = exe('python update.py ..')
    os.chdir(os.path.join(HERE, 'fc'))
    if  sys.platform == 'win32':
        stdout, stderr = exe('python setup.py --fc=gfortran --generator="MinGW Makefiles"')
    else:
        stdout, stderr = exe('python setup.py --fc=gfortran')
    os.chdir(os.path.join(HERE, 'fc', 'build'))
    if  sys.platform == 'win32':
        stdout, stderr = exe('mingw32-make')
        stdout, stderr = exe('bin\example.exe')
    else:
        stdout, stderr = exe('make')
        stdout, stderr = exe('./bin/example')
    assert 'Hello World!' in stdout
