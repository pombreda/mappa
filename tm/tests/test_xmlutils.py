# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2009 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
#     * Neither the name of the project nor the names of the contributors 
#       may be used to endorse or promote products derived from this 
#       software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
"""\
Tests against the ``xmlutils`` module.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from StringIO import StringIO
from xml.sax import saxutils
import lxml
import lxml.sax
from tm import xmlutils


def test_simplesaxhandler():
    h = lxml.sax.ElementTreeContentHandler()
    handler = xmlutils.SAXSimpleXMLWriter(h)
    handler.startDocument()
    handler.startElement('xml')
    handler.startElement('a')
    handler.characters('b')
    handler.endElement('a')
    handler.startElement('c', {'d': 'e'})
    handler.pop()
    handler.emptyElement('f')
    handler.dataElement('g', 'h')
    handler.dataElement('i', 'j', {'k': 'l'})
    handler.endElement('xml')
    handler.endDocument()

def test_simplesaxhandler2():
    out = StringIO()
    h = saxutils.XMLGenerator(out)
    handler = xmlutils.SAXSimpleXMLWriter(h)
    handler.startDocument()
    handler.startElement('xml')
    handler.startElement('a')
    handler.characters('b')
    handler.endElement('a')
    handler.startElement('c', {'d': 'e'})
    handler.pop()
    handler.emptyElement('f')
    handler.dataElement('g', 'h')
    handler.dataElement('i', 'j', {'k': 'l'})
    handler.endElement('xml')
    handler.endDocument()
    

if __name__ == '__main__':
    import nose
    nose.core.runmodule()
