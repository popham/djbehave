from django.core.management import call_command
from django.test import LiveServerTestCase
from subbehave.resource import Resource

from .base import Db

class TestServerProxy(object):

    """
    Interface to `TestServer` instances for consumption by `Command` instances.

    """
    
    def __init__(self, tc):
        """
        Stores a `LiveServerTestCase` instance to manipulate the server.

        :param tc: `LiveServerTestCase` instance for manipulating the server.
        """
        self.tc = tc

    def db_flush(self):
        """Flush the database."""
        self.tc._post_teardown()
        self.tc._pre_setup()

    def db_load_fixtures(self, fixtures):
        """
        Load fixtures (named as consumed by Django's manage.py commands).

        :param fixtures: List of fixtures to load.
        """
        for name in self._ls_test_case._databases_names(include_mirrors=False):
            call_command('loaddata', *fixtures, **{'verbosity': 0, 'database': name, 'skip_validation': True})

class TestServer(Resource):

    """
    Exposes a `TestServer` for a web client interaction.

    Implements the `Resource` interface to expose a test server. A `BehaveSuite`
    instance manages instances of `TestServer`.

    """

    def create(self):
        """Build a `TestServer` instance."""
        self.tc = LiveServerTestCase()
        self.tc.setUp()
        self.proxy = TestServerProxy(self.tc)

    def register(self, dispatcher):
        """
        Instruct `dispatcher` to provide this instance's proxy to `Db` protocol
        implementors.

        :param dispatcher: `Dispatcher` instance that provides this instance's
        proxy to `Db` protocol implementors.
        """
        dispatcher.register(lambda c: isinstance(c, Db), self.proxy)

    def destroy(self):
        """Destroy a `TestServer` instance."""
        self.tc.tearDown()
