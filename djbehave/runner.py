from django.test.runner import DiscoverRunner
from optparse import make_option
from subbehave.unittest import PyunitConsumer

from .loader import BehaveLoader

class BehaveRunner(DiscoverRunner):

    """
    `BehaveRunner` runs `Behave` on features from a `features` subdirectory.

    This implementation overrides the `Runner` and `Loader` used by
    `DiscoverRunner` with custom versions from the `subbehave` module. Further,
    the `unittest` default `test*.py` pattern has been overridden with
    `features`. Since the new pattern matches on directories instead of files,
    loading has been greatly simplified.

    """

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
        """Override the typical runner with an instance of `PyunitConsumer`."""
        return PyunitConsumer(
            verbosity=self.verbosity,
            failfast=self.failfast,
        ).run(suite)
