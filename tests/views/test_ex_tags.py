from ex_tags.templatetags.ex_tags import obfuscate_string, obfuscate_mailto, obfuscate
from tests import BaseTestCase


class ExTagsTestsCase(BaseTestCase):
    def test_obfuscate_string(self):
        r = obfuscate_string("lalala")
        self.assertEqual("&#108;&#97;&#108;&#97;&#108;&#97;", r)

    def test_obfuscate_mailto(self):
        r = obfuscate_mailto("mail@mail")
        self.assertEqual('<a href="mailto:&#109;&#97;&#105;&#108;&#64;&#109;&#97;&#105;&#108;">'
                         '&#109;&#97;&#105;&#108;&#64;&#109;&#97;&#105;&#108;</a>', r)

    def test_obfuscate(self):
        r = obfuscate("lalala")
        self.assertEqual("&#108;&#97;&#108;&#97;&#108;&#97;", r)
