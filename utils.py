import os
import sys
import subprocess
import logging
import configparser
from multiprocessing.dummy import Pool as ThreadPool

logging.basicConfig(
    format='[%(asctime)s - %(levelname)s] %(message)s',
    stream=sys.stdout)
log = logging.getLogger(__name__)

def makedir(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print('Have no permission to build a directory')
        sys.exit()

def getConfig(section, key):
    config = configparser.ConfigParser()
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'softwares.config')
    config.read(path)
    return config.get(section, key)

def out_cmd(file_name,cmd):
    with open(file_name,'w') as fh:
        fh.write(cmd)

def run_shell_cmd(cmd):
    run = subprocess.run(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if run.returncode == 0:
        print("STDOUT:", run.stdout)
    else:
        print("STDOUT:", run.stdout)
        print("STDERR:", run.stderr)

def multi_run(func,cmds,jobs,maxc):
    ## split command into sub-commands,
    ## each sub-command has {jobs} tasks
    ## run {jobs} tasks parallelly to save time
    if isinstance(cmds,list):
        for i in range(0, len(cmds), jobs):
            subcmds = cmds[i:i + jobs]
            pool = ThreadPool(maxc)
            pool.map(func, subcmds)
            pool.close()
            pool.join()
    elif isinstance(cmds,str):
        new_cmds = [cmds]
        pool = ThreadPool(maxc)
        pool.map(func, new_cmds)
        pool.close()
        pool.join()