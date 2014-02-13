import os
from setuptools import find_packages, setup

#packages, data_files = [], []
#root_dir = os.path.dirname(__file__)
#if root_dir:
#    os.chdir(root_dir)
#for dirpath, dirnames, filenames in os.walk('pkg'):
    # Ignore dirnames that start with '.'
#    for i, dirname in enumerate(dirnames):
#        if dirname.startswith('.'): del dirnames[i]
#    if '__init__.py' in filenames:
#        pkg = dirpath.replace(os.path.sep, '.')
#        if os.path.altsep:
#            pkg = pkg.replace(os.path.altsep, '.')
#        packages.append(pkg)
#    elif filenames:
#        prefix = dirpath[4:] # Strip leading 'pkg'
#        for f in filenames:
#            data_files.append(os.path.join(prefix, f))

setup(
    name="Djbehave",
    description="Integration of Behave into Django's command line interface.",
    version=VERSION,
    author="Tim Popham",
    author_email="popham@uw.edu",
    url="https://github.com/popham/djbehave",
    download_url="https://github.com/popham/djbehave/...",
    package_dir={'djbehave': 'pkg'},
    packages=packages,
    package_data={'djbehave': data_files},
    include_package_data=True,
    install_requires=[
        'django>=1.4.1',
        #    'python3.3'
        #    'subbehave'
            'behave>=1.2.3'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'],
    keywords='behave djbehave subbehave django gherkin'
)
