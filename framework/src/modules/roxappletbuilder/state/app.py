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

from roxappletbuilder.state.states import State
import gtk
import logging

class StateApp(object):

    def __init__(self, name, states):
        self.name = name
        self._monitors = []
        self.states = states
        self._rootWidget = None

        self._parseOptions()

    def _exitApp(self):
        self._tearDownMonitors()

        import sys

        # TODO is there some kind of gtk.quit()?
        sys.exit(0)

    def _tearDownMonitors(self):
        for m in self._monitors:
            m.tearDown()
        self._monitors = []

    def _exitAppRequest(self, event):
        self._exitApp()

    def _switchState(self, event):
        self.applyNextState()

    def _createMenu(self):
        m = gtk.Menu()

        exit = gtk.MenuItem('Exit')
        m.append(exit)
        exit.connect('activate', self._exitAppRequest)
        exit.show_all()

        return m

    def __contextMenuCallback(self, widget, event):
        if((event.type == gtk.gdk.BUTTON_PRESS) and (event.button == 3)):
            widget.popup(None, None, None, event.button, event.time)
            
            return True
            
        return False

    def _parseOptions(self):
        from optparse import OptionParser

        parser = OptionParser()
    
        (options, args) = parser.parse_args()

        if(len(args) == 0):
            self.xid = None
        else:
            self.xid = int(args[0])

    def showState(self, state):
        self.activeState = state

        # TODO put into separate method
        pixBuf = gtk.gdk.pixbuf_new_from_file(state.iconPath)
        # TODO specify icon res somehow dynamically
        pixBuf = pixBuf.scale_simple(32, 16, gtk.gdk.INTERP_BILINEAR)
        stateImage = gtk.Image()
        stateImage.set_from_pixbuf(pixBuf)

        self.switch.set_image(stateImage)

    def reloadState(self):
        currentState = self._determineActiveState()

        self.showState(currentState)

    def applyState(self, state):
        # TODO indicate state change in UI
        # TODO do non UI blocking state activation
        state.activate()

        self.showState(state)

    def applyNextState(self):
        i = self.states.index(self.activeState)

        newState = self.states[(i + 1) % len(self.states)]

        self.applyState(newState)

    @property
    def rootWidget(self):
        if(self._rootWidget is None):
            menu = self._createMenu()

            self.switch = gtk.Button()
            self.switch.connect('clicked', self._switchState)
            self.switch.connect_object('button-press-event', self.__contextMenuCallback, menu)

            self.reloadState()

            self._rootWidget = self.switch

            #m = PollMonitor(self)
            #self._monitors.append(m)
            #m.setUp()

        return self._rootWidget
