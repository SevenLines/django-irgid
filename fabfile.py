from fabric.api import run, env, cd, prefix, settings
from fabric.operations import local

env.hosts = ['phosphorus.locum.ru']
env.user = 'hosting_mmailm'
env.activate = 'source /home/hosting_mmailm/projects/env-irgid/bin/activate'

app_dir = "/home/hosting_mmailm/projects/django-irgid"


def build_production():
    local("git checkout master")
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
            run("python manage.py update_settings")
            run("touch django.wsgi")


def download(only_base=False):
    # download database backup from server
    local("scp -C {user}@{host}:{app_dir}/dump.tgz dump.tgz".format(
        user=env.user, host=env.hosts[0], app_dir=app_dir)
    )
    if not only_base:
        # download media backup from server
        local("scp -C {user}@{host}:{app_dir}/media.tgz media.tgz".format(
            user=env.user, host=env.hosts[0], app_dir=app_dir)
        )

def backup(only_base=False):
    local("ssh-add ~/.ssh/locum.ru")  # add ssh-key

    # create backip_archive on server
    with cd(app_dir):
        with prefix(env.activate):
            run("python manage.py dumpdata > dump.json")
            run("tar cvzf dump.tgz dump.json")
        if not only_base:
            run("tar -czf media.tgz media")  # create media dump

    # remove local old backup
    local("rm -f dump.json")
    if not only_base:
        local("rm -f media.tgz")

    download(only_base)

    # restore database
    local("tar xvzf dump.tgz")  # unpack archive
    local("python manage.py sqlflush | python manage.py dbshell")  # clear old data
    local("python manage.py loaddata dump.json")  # load new data

    if not only_base:
        # restore media
        local("rm -rf media")
        local("mkdir media")
        local("tar -xf media.tgz")
