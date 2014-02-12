from django.test.runner import DiscoverRunner
from optparse import make_option
from subbehave.unittest import PyunitRunner

from .loader import BehaveLoader

class BehaveRunner(DiscoverRunner):
    test_loader = BehaveLoader()
    option_list = (
        make_option('-t', '--top-level-directory',
            action='store', dest='top_level', default=None,
            help='Top level of project for feature discovery.'),
        make_option('-p', '--pattern',
            action='store', dest='pattern', default='features',
            help='The test matching pattern. Defaults to features.'),
        )

    def run_suite(self, suite, **kwargs):
        return PyunitRunner(
            verbosity=self.verbosity,
            failfast=self.failfast,
        ).run(suite)
