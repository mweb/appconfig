import os
import multiprocessing

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [ 'appdirs',
        ]
tests_requires = [ 'nose',
        ]

setup(name='appconfig',
        version='0.5',
        description='An easy to use config file wrapper.',
        long_description=README + '\n\n' + CHANGES,
        classifiers=[
            "Programming Language :: Python",
            "Topic :: ",
            ],
        author='Mathias Weber',
        author_email='mathew.weber@gmail.com',
        license='BSD',
        url='',
        test_suite='nose.collector',
        packages=find_packages(),
        install_requires=requires,
        tests_require=tests_requires)
