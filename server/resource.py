from django.core.management import call_command
from django.test import LiveServerTestCase
from subbehave.resource import Resource

from .base import Db

class TestServerProxy(object):
    def __init__(self, tc):
        self.tc = tc

    def db_flush(self):
        self.tc._post_teardown()
        self.tc._pre_setup()

    def db_load_fixtures(self, fixtures):
        for name in self._ls_test_case._databases_names(include_mirrors=False):
            call_command('loaddata', *fixtures, **{'verbosity': 0, 'database': name, 'skip_validation': True})

class TestServer(Resource):
    def create(self):
        self.tc = LiveServerTestCase()
        self.tc.setUp()
        self.proxy = TestServerProxy(self.tc)

    def register(self, dispatcher):
        dispatcher.register(lambda c: isinstance(c, Db), self.proxy)

    def destroy(self):
        pass
