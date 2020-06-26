### jack.version: define program version and name for
### jack - extract audio from a CD and encode it using 3rd party software
### Copyright (C) 2002  Arne Zellentin <zarne@users.sf.net>

### This program is free software; you can redistribute it and/or modify
### it under the terms of the GNU General Public License as published by
### the Free Software Foundation; either version 2 of the License, or
### (at your option) any later version.

### This program is distributed in the hope that it will be useful,
### but WITHOUT ANY WARRANTY; without even the implied warranty of
### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
### GNU General Public License for more details.

### You should have received a copy of the GNU General Public License
### along with this program; if not, write to the Free Software
### Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import sys

name      = "jack"
version   = "4.0.0"

author    = "Arne Zellentin"
copyright = "(C)2020 " + author
email     = "zarne@users.sf.net"
devemail  = "<%s>" % email

license   = "GPLv2"

url       = "https://github.com/zzarne/jack"

rcversion = 31

py_version = sys.version.split()[0]