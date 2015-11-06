from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import MULTIPART_CONTENT


class TestCaseEx(TestCase):
    def get(self, path, data=None, follow=False, secure=False, **extra):
        return self.client.get(path, data, follow, secure, **extra)

    def post(self, path, data=None, content_type=MULTIPART_CONTENT, follow=False, secure=False, **extra):
        return self.client.post(path, data, content_type, follow, secure, **extra)

    def api(self, name, data=None, post=True, content_type=MULTIPART_CONTENT, follow=False, secure=False, **extra):
        if post:
            result = self.post(reverse(name), data=data, content_type=content_type, follow=follow, secure=secure,**extra)
        else:
            result = self.get(reverse(name), data=data, follow=follow, secure=secure, **extra)
        return result
