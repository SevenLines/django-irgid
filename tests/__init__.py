from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.test.testcases import TestCase


class LoggedSession(object):
    def __init__(self, client, username, password):
        self.client = client
        self.username = username
        self.password = password

    def __enter__(self):
        return self.client.login(username=self.username, password=self.password)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.logout()


class BaseTestCase(TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.superuser = User.objects.create_superuser('admin', 'admin@mail.com', '1234')
        call_command('update_settings')

    def api(self, name, data=None, params=None, status_code=200, post=None):
        if not post:
            r = self.client.get(reverse(name, kwargs=params), data=data)
        else:
            r = self.client.post(reverse(name, kwargs=params), data=data)
        self.assertEqual(r.status_code, status_code)
        return r

    def login(self, username='admin', password='1234'):
        return LoggedSession(self.client, username, password)
