import os
from setuptools import find_packages, setup

version = '0.0.1.0'

description = """
Djbehave exposes `Behave <http://pythonhosted.org/behave/>`_ for use under `Django <https://www.djangoproject.com/>`_.
It provides a `manage.py behave` analogue to Django's `manage.py test` command, maintaining the feel of Django's unittest interface.
"""

setup(
    name="djbehave",
    description="Integration of Behave into Django's command line interface.",
    version="%s" % version,
    author="Tim Popham",
    author_email="popham@uw.edu",
    url="https://github.com/popham/djbehave",
    download_url="https://github.com/popham/djbehave/archive/%s.tar.gz" % version,
    packages=find_packages('.', exclude=()),
    install_requires=[
        'django>=1.4.1',
        'subbehave==%s' % version,
        'behave>=1.2.3'],
    license="MIT",
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
    long_description = description,
    keywords='behave djbehave subbehave django gherkin')
