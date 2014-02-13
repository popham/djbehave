from subbehave.command import Command, Complete, InjectResource

from .base import Db
from .resource import TestServer

class CreateTestServer(InjectResource):

    """
    Injects a test server into a `BehaveSuite` instance.

    """

    def __call__(self, return_queue, owner):
        """Implements the `InjectResource` protocol."""
        ts = TestServer()
        owner.attachResource(ts)
        self.vacuous_return(return_queue)

class LoadFixtures(Db):

    """
    Loads fixtures into the test database.

    """

    def __init__(self, fixtures):
        """
        Build a `LoadFixtures` command instance.

        :param fixtures: List of fixtures to load (named as consumed by Django's
        manage.py commands)
        """
        if isinstance(fixtures, str):
            fixtures = [fixtures]
        self.fixtures = fixtures

    def __call__(self, return_queue, proxy):
        """Implements the `Db` protocol."""
        proxy.db_load_fixtures(self.fixtures)
        self.vacuous_return(return_queue)

class Flush(Db):

    """
    Flushes the test database.

    """

    def __call__(self, return_queue, proxy):
        """Implements the `Db` protocol."""
        proxy.db_flush()
        self.vacuous_return(return_queue)
