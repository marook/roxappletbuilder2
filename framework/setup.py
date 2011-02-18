#!/usr/bin/env python
#
# Copyright 2009 Peter Prohaska
#
# This file is part of roxappletbuilder2.
#
# This file is a fork of of tagfs. See
# http://github.com/marook/tagfs/
#
# roxappletbuilder2 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# roxappletbuilder2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with roxappletbuilder2.  If not, see <http://www.gnu.org/licenses/>.
#

from distutils.core import setup, Command
import sys
import os
from os.path import (
        basename,
        dirname,
        abspath,
        splitext,
        join as pjoin
)
from glob import glob
from unittest import TestLoader, TextTestRunner
import re
import datetime

projectdir = dirname(abspath(__file__))
reportdir = pjoin(projectdir, 'reports')

srcdir = pjoin(projectdir, 'src')
moddir = pjoin(srcdir, 'modules')
testdir = pjoin(srcdir, 'test')

class Report(object):

    def __init__(self):
        self.reportDateTime = datetime.datetime.utcnow()
        self.reportDir = os.path.join(reportdir, self.reportDateTime.strftime('%Y-%m-%d_%H_%M_%S'))
        
        # fails when dir already exists which is nice
        os.makedirs(self.reportDir)

    @property
    def coverageReportFileName(self):
        return os.path.join(self.reportDir, 'coverage.txt')

    @property
    def unitTestReportFileName(self):
        return os.path.join(self.reportDir, 'tests.txt')

def sourceFiles():
    yield os.path.join(bindir, 'roxappletbuilder2')
    
    sourceFilePattern = re.compile('^.*[.]py$')
    for root, dirs, files in os.walk(moddir):
        for f in files:
            if(not sourceFilePattern.match(f)):
                continue

            yield os.path.join(root, f)

def printFile(fileName):
    if(not os.path.exists(fileName)):
        # TODO maybe we should not silently return?
        return

    with open(fileName, 'r') as f:
        for line in f:
            sys.stdout.write(line)

class test(Command):
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        self._cwd = os.getcwd()
        self._verbosity = 2

    def finalize_options(self): pass

    def run(self):
        report = Report()

        testPyMatcher = re.compile('(.*/)?test[^/]*[.]py', re.IGNORECASE)

        tests = ['.'.join([
                basename(testdir), splitext(basename(f))[0]
        ]) for f in glob(pjoin(
                testdir, '*.py'
        )) if testPyMatcher.match(f)]

        print "..using:"
        print "  testdir:", testdir
        print "  tests:", tests
        print "  sys.path:", sys.path
        print
        sys.path.insert(0, moddir)
        sys.path.insert(0, srcdir)

        # configure logging
        # TODO not sure how to enable this... it's a bit complicate to enable
        # logging only for 'make mt' and disable it then for
        # 'python setup.py test'. 'python setup.py test' is such a gabber...
        #if 'DEBUG' in os.environ:
        #    from tagfs import log_config
        #    log_config.setUpLogging()

        suite = TestLoader().loadTestsFromNames(tests)

        with open(report.unitTestReportFileName, 'w') as testResultsFile:
            r = TextTestRunner(stream = testResultsFile, verbosity = self._verbosity)

            def runTests():
                r.run(suite)

            try:
                import coverage

                c = coverage.coverage()
                c.start()
                runTests()
                c.stop()
    
                with open(report.coverageReportFileName, 'w') as reportFile:
                    c.report([f for f in sourceFiles()], file = reportFile)

            except ImportError:
                print ''
                print 'coverage module not found.'
                print 'To view source coverage stats install http://nedbatchelder.com/code/coverage/'
                print ''

                runTests()

        # TODO use two streams instead of printing files after writing
        printFile(report.unitTestReportFileName)
        printFile(report.coverageReportFileName)

# Overrides default clean (which cleans from build runs)
# This clean should probably be hooked into that somehow.
class clean_pyc(Command):
    description = 'remove *.pyc files from source directory'
    user_options = []

    def initialize_options(self):
        self._delete = []
        for cwd, dirs, files in os.walk(projectdir):
            self._delete.extend(
                pjoin(cwd, f) for f in files if f.endswith('.pyc')
            )

    def finalize_options(self):
        pass

    def run(self):
        for f in self._delete:
            try:
                os.unlink(f)
            except OSError, e:
                print "Strange '%s': %s" % (f, e)
                # Could be a directory.
                # Can we detect file in use errors or are they OSErrors
                # as well?
                # Shall we catch all?

setup(
    cmdclass = {
        'test': test,
        'clean_pyc': clean_pyc,
    },
    name = 'roxappletbuilder2',
    version = '2.0.0',
    url = 'TODO',
    description = '',
    long_description = '',
    author = 'Markus Pielmeier',
    author_email = 'markus.pielmeier@googlemail.com',
    license = 'GPLv3',
    platforms = 'Linux',
    requires = [],
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python'
    ],
    data_files = [
        (pjoin('share', 'doc', 'tagfs'), ['AUTHORS', 'COPYING'])
    ],
    # TODO maybe we should include src/bin/*?
    #scripts = [pjoin(bindir, 'tagfs')],
    packages = ['roxappletbuilder'],
    package_dir = {'': moddir},
)
