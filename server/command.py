from subbehave.command import Command, Complete, Resource

from .base import Db
from .resource import TestServer

class CreateTestServer(Resource):
    def __call__(self, return_queue, owner):
        ts = TestServer()
        owner.attachResource(ts)
        self.vacuous_return(return_queue)

class LoadFixtures(Db):
    def __init__(self, fixtures):
        if isinstance(fixtures, str):
            fixtures = [fixtures]
        self.fixtures = fixtures

    def __call__(self, return_queue, proxy):
        proxy.db_load_fixtures(self.fixtures)
        self.vacuous_return(return_queue)

class Flush(Db):
    def __call__(self, return_queue, proxy):
        proxy.db_flush()
        self.vacuous_return(return_queue)
