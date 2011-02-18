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

from roxappletbuilder.log import setUpLogging
import gtk

def main(app):
    setUpLogging(app.name)

    if(app.xid is None):
        w = gtk.Window()
        w.add(app.rootWidget)
        w.show_all()
    
    else:
        xid = app.xid
    
        logging.debug('Connecting to XID ' + str(xid))
    
        p = gtk.Plug(xid)
        p.add(app.rootWidget)
        p.show_all()

    gtk.main()
