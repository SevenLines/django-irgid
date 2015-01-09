from fabric.api import run, env, cd, prefix, settings
from fabric.operations import local

env.hosts = ['phosphorus.locum.ru']
env.user = 'hosting_mmailm'
env.activate = 'source /home/hosting_mmailm/projects/env-irgid/bin/activate'

app_dir = "/home/hosting_mmailm/projects/django-irgid"


def build_production():
    local("git checkout master")
    local("git merge -X theirs dev")
    local("git merge --no-ff dev")
    # minify()
    # with settings(warn_only=True):
    # local("git commit -a -m 'minify scripts and css'")
    # local("git checkout production")
    # local("git merge --no-edit master")
    local("git checkout dev")


def deploy():
    build_production()
    local("ssh-add ~/.ssh/locum.ru")
    local("git push --all -u")
    with cd(app_dir):
        with prefix(env.activate):
            # run("git stash")
            run("git pull")
            with settings(warn_only=True):
                # run("git stash apply")
                run('pip-accel install -r requirements.txt')
            run("python manage.py migrate")
            run("python manage.py collectstatic --noinput")
            run("touch django.wsgi")