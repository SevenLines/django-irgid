from fabric.api import run, env, cd, prefix, settings
from fabric.operations import local

env.hosts = ['phosphorus.locum.ru']
env.user = 'hosting_mmailm'
env.activate = 'source /home/hosting_mmailm/projects/env/bin/activate'

def deploy():
    pass