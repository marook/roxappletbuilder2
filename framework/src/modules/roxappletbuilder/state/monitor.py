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

class Monitor(object):

    def __init__(self, app):
        self.app = app

    def setUp(self):
        pass

    def tearDown(self):
        pass

class PollMonitor(Monitor):

    # TODO synchronize self.timer access

    def _reloadState(self):
        self.timer = None

        logging.debug('PollMonitor is reloading state')

        gtk.gdk.threads_enter()
        try:
            self.app.reloadState()
        finally:
            gtk.gdk.threads_leave()

        self._scheduleReload()

    def _scheduleReload(self):
        import threading

        self.timer = threading.Timer(10.0, self._reloadState)
        self.timer.start()

    def setUp(self):
        logging.debug('Launching poll monitor')

        self._scheduleReload()

    def tearDown(self):
        if(not self.timer is None):
            self.timer.cancel()
