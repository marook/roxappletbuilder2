#!/usr/bin/env python
#
# Copyright 2011 Markus Pielmeier
#
# This file is part of roxappletbuilder2.
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

import unittest
from roxappletbuilder.resource import ResourceResolver
import os.path

class ResourceResolverConstructorTests(unittest.TestCase):

    def testAppletRunFileIsDirFail(self):
        self.assertRaises(Exception, ResourceResolver.__init__, '.')

    def testAppletRunFileIsNoneFail(self):
        self.assertRaises(Exception, ResourceResolver.__init__, None)

class ResourceResolverConstructorTests(unittest.TestCase):

    def setUp(self):
        self.rr = ResourceResolver(__file__)

    def testRelativeResourcePathIsNoneFail(self):
        self.assertRaises(Exception, self.rr.getResourcePath, None)

    def testRelativeResourcePathIsAbsoluteFail(self):
        
        self.assertRaises(Exception, self.rr.getResourcePath, os.path.abspath('.'))

    def testRelativeResourcePathResolve(self):
        demoResPath = self.rr.getResourcePath('demoResource.txt')

        self.assertTrue('Invalid path %s' % demoResPath, os.path.exists(demoResPath))
