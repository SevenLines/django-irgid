from tests import TestCaseEx


class ExcursionsCategoryTestCase(TestCaseEx):
    def test_main_page(self):
        r = self.api('index')
