import os
from fnmatch import fnmatch
from unittest.loader import TestLoader, _make_failed_load_tests
from unittest.suite import TestSuite

from subbehave.unittest.suite import BehaveSuite

class BehaveLoader(TestLoader):

    """
    Load features from a `features` directory, unless an alternate match pattern
    has been provided.

    The loader uses the `TestSuite` class from unittest. This suite wraps a
    single `BehaveSuite` instance. The `BehaveSuite` instance was not intended
    to provide its tests to another suite, requiring the extra wrapper.

    """

    suiteClass = TestSuite

    def discover(self, start_dir, pattern='features', top_level_dir=None):
        """
        Override the default pattern of the method's signature with 'features'
        """
        return super().discover(start_dir, pattern, top_level_dir)

    def _find_tests(self, start_dir, pattern):
        paths = os.listdir(start_dir)

        for path in paths:
            full_path = os.path.join(start_dir, path)
            if os.path.isdir(full_path):
                if not os.path.isfile(os.path.join(full_path, '__init__.py')):
                    continue

                load_tests = None
                tests = None
                if fnmatch(path, pattern):
                    # Check for load_tests under matching directories
                    name = self._get_name_from_path(full_path)
                    package = self._get_module_from_name(name)
                    load_tests = getattr(package, 'load_tests', None)
                    tests = BehaveSuite(full_path)

                if load_tests is None:
                    if tests is not None:
                        # tests loaded from package file
                        yield tests
                    # recurse into the package
                    for test in self._find_tests(full_path, pattern):
                        yield test
                else:
                    try:
                        yield load_tests(self, tests, pattern)
                    except Exception as e:
                        yield _make_failed_load_tests(package.__name__, e, TestSuite)
