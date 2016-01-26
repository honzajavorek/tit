
import sys
import subprocess

from setuptools import setup
from setuptools.command.test import test


def readme():
    with open('README.rst') as f:
        return f.read()


class TestCommand(test):
    def run(self):
        test.run(self)
        sys.exit(subprocess.call(['flake8', 'tit.py', 'setup.py']))


setup(
    name='tit',
    description='Better titulky.com search',
    long_description=readme(),
    version='0.0.2',
    url='http://github.com/honzajavorek/tit',
    author='Honza Javorek',
    author_email='mail@honzajavorek.cz',
    license='MIT',
    py_modules=['tit'],
    install_requires=[
        'click',
        'cssselect',
        'requests',
        'lxml',
        'sh',
    ],
    tests_require=[
        'flake8',
    ],
    entry_points='''
        [console_scripts]
        tit=tit:cli
    ''',
    cmdclass={
        'test': TestCommand,
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Multimedia :: Video',
    ],
    keywords='subtitles titulky.com csfd.cz',
)
