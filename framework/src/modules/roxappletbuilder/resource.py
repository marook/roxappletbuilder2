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

import os.path

def resolveAppDirectory(appletRunFile):
    d = os.path.dirname(os.path.abspath(appletRunFile))

    assert os.path.isdir(d), '%s should be the app directory!' % d

    return d

class ResourceResolver(object):

    def __init__(self, appletRunFile):
        self.resourceDirectory = resolveAppDirectory(appletRunFile)

    def getResourcePath(self, relativeResourcePath):
        if(os.path.isabs(relativeResourcePath)):
               raise ValueError()

        return os.path.join(self.resourceDirectory, relativeResourcePath)
