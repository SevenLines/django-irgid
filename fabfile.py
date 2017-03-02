from fabric.api import run, env, cd, prefix, settings
from fabric.operations import local

env.hosts = ['83.220.170.91']
env.user = 'light'
env.activate = 'source ~/.virtualenvs/irgid-django/bin/activate'
env.use_ssh_config = True

app_dir = "~/projects/irgid-django"


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
    local("git push --all -u")
    with cd(app_dir):
        with prefix(env.activate):
            # run("git stash")
            run("git pull")
            with settings(warn_only=True):
                # run("git stash apply")
                run('pip install -r requirements.txt')
            run("python manage.py migrate")
            run("python manage.py collectstatic --noinput")
            run("python manage.py update_settings")
            run("touch uwsgi.ini --no-dereference")


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
    restore_db()

    if not only_base:
        # restore media
        local("rm -rf media")
        local("mkdir media")
        local("tar -xf media.tgz")


def restore_db():
    # restore database
    local("tar xvzf dump.tgz")  # unpack archive
    local("python manage.py sqlflush | python manage.py dbshell")  # clear old data
    local("python manage.py loaddata dump.json")  # load new data
