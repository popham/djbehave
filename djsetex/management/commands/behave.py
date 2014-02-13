import logging
import sys
import os
from optparse import make_option, OptionParser

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.encoding import force_str

def get_runner(settings, test_runner_class=None):
    """
    Provide an instance of test_runner_class if provided, otherwise use the
    runner from the settings module.

    :param test_runner_class: Optional string prescribing the runner to user
    (dotted module syntax resolvable from the path).
    :returns: `TestRunner` class.
    """
    if not test_runner_class:
        test_runner_class = settings.BEHAVE_RUNNER

    test_path = test_runner_class.split('.')
    test_module_name = '.'.join(test_path[:-1])
    test_module = __import__(test_module_name, {}, {}, force_str(test_path[-1]))
    test_runner = getattr(test_module, test_path[-1])
    return test_runner

class Command(BaseCommand):

    """
    Replicate Behave's CLI in Django's manage.py framework.

    Imitate the implementation from Django's core.management.command.test
    implementation, but reparametrized for `BehaveRunner`.

    """

    option_list = BaseCommand.option_list + (
        make_option('--failfast',
            action='store_true', dest='failfast', default=False,
            help='Tells Django to stop running the test suite after first '
                 'failed test.'),
        make_option('--behaverunner',
            action='store', dest='behaverunner',
            help='Tells Django to use specified test runner class instead of '
                 'the one specified by the BEHAVE_RUNNER setting.'),
        make_option('--liveserver',
            action='store', dest='liveserver', default=None,
            help='Overrides the default address where the test server (used '
                 'with the TestServer resouce) is expected to run from. The '
                 'default value is localhost:8081.'),
        make_option('--exclude',
            action='store', dest='exclude_re', default=None,
            help='Do not run feature files matching the provided regular '
                 'expression pattern.'),
        make_option('--include',
            action='store', dest='include_re', default=None,
            help='Only run feature files matching the provided regular '
                 'expression pattern.'),
        make_option('--name',
            action='append', dest='name', default=None,
            help='Only execute the feature elements which match part of the '
                 'given name. If this option is given more than once, it will '
                 'match against all the given names.'),
        make_option('--stop',
            action='store_true', dest='stop', default=False,
            help='Stop running tests at the first failure.'),
        make_option('--wip',
            action='store_true', dest='wip', default=False,
            help='Only run scenarios tagged with "wip".'),
        make_option('--expand',
            action='store_true', dest='expand', default=False,
            help='Expand scenario outline tables in output.'),
#        make_option('--lang',
#            action='store', dest='lang', default=None,
#            help='Use keywords for a language other than English.'),
#        make_option('--lang-list',
#            action='store_true', dest='lang_list', default=False,
#            help='List the languages available for --lang.'),
#        make_option('--lang-help',
#            action='store_true'?, dest='lang_help', default=False?,
#            help='List the translations accepted for one language.'),
        make_option('--tags-help',
            action='store_true', dest='tags_help', default=False,
            help='Show help for tag expressions.'),
#on parent(?)        make_option('--version',
#            action='store_true', dest='version', default=False,
#            help='Show version.'),
        make_option('--tags',
            action='append', dest='tags',
            help='Only execute features or scenarios with tags matching the '
                 'provided tags. Pass \'--tags-help\' for more information.'),
        )
    help = ('Discover and run tests in the specified modules or the current directory.')
    args = '[path.to.modulename|path.to.modulename.TestCase|path.to.modulename.TestCase.test_method]...'

    requires_model_validation = False

    def __init__(self):
        self.test_runner = None
        super(Command, self).__init__()

    def run_from_argv(self, argv):
        """
        Pre-parse the command line to extract the value of the --testrunner
        option. This allows a test runner to define additional command line
        arguments.
        """
        option = '--behaverunner='
        for arg in argv[2:]:
            if arg.startswith(option):
                self.test_runner = arg[len(option):]
                break
        super(Command, self).run_from_argv(argv)

    def create_parser(self, prog_name, subcommand):
        test_runner_class = get_runner(settings, self.test_runner)
        options = self.option_list + getattr(
            test_runner_class, 'option_list', ())
        return OptionParser(prog=prog_name,
                            usage=self.usage(subcommand),
                            version=self.get_version(),
                            option_list=options)

    def execute(self, *args, **options):
        if int(options['verbosity']) > 0:
            # ensure that deprecation warnings are displayed during testing
            # the following state is assumed:
            # logging.capturewarnings is true
            # a "default" level warnings filter has been added for
            # DeprecationWarning. See django.conf.LazySettings._configure_logging
            logger = logging.getLogger('py.warnings')
            handler = logging.StreamHandler()
            logger.addHandler(handler)
        super(Command, self).execute(*args, **options)
        if int(options['verbosity']) > 0:
            # remove the testing-specific handler
            logger.removeHandler(handler)

    def handle(self, *test_labels, **options):
        from django.conf import settings

        BehaveRunner = get_runner(settings, options.get('behaverunner'))
        options['verbosity'] = int(options.get('verbosity'))

        if options.get('liveserver') is not None:
            os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = options['liveserver']
            del options['liveserver']

        behave_runner = BehaveRunner(**options)
        failures = behave_runner.run_tests(test_labels)

        if failures:
            sys.exit(bool(failures))
