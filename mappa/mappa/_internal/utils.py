# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2011 -- Lars Heuer - Semagia <http://www.semagia.com/>.
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
Mappa's internal utilities.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from itertools import chain
from uuid import uuid4
from tm.xmlutils import is_ncname

def random_id():
    return uuid4().int

def topic_id(base, topic):
    """\
    Returns an identifier for the provided topic.
    """
    ident = None
    for loc in chain(topic.iids, topic.sids):
        if not loc.startswith(base) or not '#' in loc:
            continue
        ident = loc[loc.index('#')+1:]
        if ident.startswith('t-'):
            ident = None
            continue
        break
    if not ident:
        ident = topic.id
    if ident and is_ncname(unicode(ident)):
        return ident
    return 't-%s' % topic.id

def is_slo(string):
    """\
    Returns if the string represents a subject locator.
    Subject locators start with "="
    """
    return string[0] == '='

def strip_slo_prefix(string):
    """\
    
    """
    return string[1:].strip()

def is_uri(string):
    """\
    Returns if the string represents a URI.
    
    Note that this function just checks if a colon ``:`` is present.
    """
    return ':' in string

def make_locator(base, frag):
    from mappa import irilib
    return irilib.resolve_iri(base, '#' + frag)