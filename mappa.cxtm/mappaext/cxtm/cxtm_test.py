# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Utility functions to run CXTM tests.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
import os
import codecs
import mappa
from StringIO import StringIO
from tm import Source
from tm.mio import MIOException
from mappa import ModelConstraintViolation
from .cxtm1 import CXTMTopicMapWriter
from mappa.miohandler import MappaMapHandler

_CXTM_TRUNK = u'cxtm-tests-code-179-trunk.zip'


def get_baseline(filename):
    """\
    Returns the CXTM baseline path for the provided filename.
    """
    return os.path.abspath(os.path.dirname(filename) + '/../baseline/%s.cxtm' % os.path.basename(filename))


def _download_cxtm_tests():
    from zipfile import ZipFile
    import urllib, shutil
    directory = os.path.abspath('./cxtm/')
    archive_name = os.path.join(directory, 'cxtm-tests.zip')
    sf_filename = _CXTM_TRUNK
    urllib.urlretrieve('http://sourceforge.net/code-snapshots/svn/c/cx/cxtm-tests/code/%s' % sf_filename, archive_name)
    archive = ZipFile(archive_name)
    archive.extractall(directory)
    archive.close()
    trunk_dir = os.path.join(directory, sf_filename[:sf_filename.rindex(u'.')])
    for f in os.listdir(trunk_dir):
        subdir = os.path.join(trunk_dir, f)
        if os.path.isdir(subdir) and f != 'web':
            target = os.path.join(directory, f)
            shutil.move(subdir, target)
    shutil.rmtree(trunk_dir)


def find_cxtm_cases(directory, extension, subdir, exclude=None):
    """\

    """
    exclude = set(exclude or [])
    directory = os.path.abspath('./cxtm/%s/%s' % (directory, subdir))
    if not os.path.exists(directory):
        _download_cxtm_tests()
    for filename in (n for n in os.listdir(directory) if n.endswith(extension) and n not in exclude):
        yield os.path.join(directory, filename)


def find_valid_cxtm_cases(directory, extension, exclude=None):
    """\

    """
    return find_cxtm_cases(directory, extension, 'in', exclude)


def find_invalid_cxtm_cases(directory, extension, exclude=None):
    """\

    """
    return find_cxtm_cases(directory, extension, 'invalid', exclude)


def create_invalid_cxtm_cases(factory, directory, extension, exclude=None):
    """\
    Returns a generator for invalid CXTM test cases.

    `factory`
        A callable which returns a IDeserializer instance.
    `directory`
        The main directory for the tests, i.e. 'ctm'
    `extension`
        The filename extension
    `exclude`
        An interable of filename which should not be evaluated or ``None``.
    """
    for filename in find_invalid_cxtm_cases(directory, extension, exclude):
        yield check_invalid, factory(), filename


def create_valid_cxtm_cases(factory, directory, extension, post_process=None, exclude=None):
    """\
    Returns a generator for valid CXTM test cases.

    `factory`
        A callable which returns a IDeserializer instance.
    `directory`
        The main directory for the tests, i.e. 'ctm'
    `extension`
        The filename extension
    `exclude`
        An interable of filename which should not be evaluated or ``None``.
    `post_process`
        A callable which postprocesses the topic map or ``None``.
    """
    for filename in find_valid_cxtm_cases(directory, extension, exclude):
        yield check_valid, factory(), filename, post_process


def create_writer_cxtm_cases(writer_factory, deserializer_factory, directory, extension, post_process=None, exclude=None):
    """\
    Returns a generator for valid CXTM test cases.

    `writer_factory`
        A callable which returns a IWriter instance.
    `deserializer_factory`
        A callable which returns a IDeserializer instance.
    `directory`
        The main directory for the tests, i.e. 'ctm'
    `extension`
        The filename extension
    `exclude`
        An interable of filename which should not be evaluated or ``None``.
    `post_process`
        A callable which postprocesses the topic map or ``None``.
    """
    for filename in find_valid_cxtm_cases(directory, extension, exclude):
        yield check_writer, writer_factory, deserializer_factory, filename, post_process


def fail(msg):
    """\

    """
    raise AssertionError(msg)


def check_writer(writer_factory, deser_factory, filename, post_process):
    conn = mappa.connect()
    tm = conn.create('http://www.semagia.com/mappa-test-tm')
    # 1. Read the source
    src = Source(file=open(filename, 'rb'))
    deserializer = deser_factory()
    deserializer.handler = MappaMapHandler(tm)
    deserializer.parse(src)
    if post_process:
        post_process(tm)
    # 2. Write the topic map
    out = StringIO()
    writer = writer_factory(out, src.iri)
    writer.write(tm)
    # 3. Read the generated topic map
    tm2 = conn.create('http://www.semagia.com/mappa-test-tm2')
    src2 = Source(data=out.getvalue(), iri=src.iri)
    deserializer = deser_factory()
    deserializer.handler = MappaMapHandler(tm2)
    deserializer.parse(src2)
    if post_process:
        post_process(tm2)
    # 4. Generate the CXTM
    f = codecs.open(get_baseline(filename), encoding='utf-8')
    expected = f.read()
    f.close()
    result = StringIO()
    c14n = CXTMTopicMapWriter(result, src.iri)
    c14n.write(tm2)
    res = unicode(result.getvalue(), 'utf-8')
    if expected != res:
        fail('failed: %s.\nExpected: %s\nGot: %s\nGenerated topic map: %s' % (filename, expected, res, out.getvalue()))


def check_valid(deserializer, filename, post_process=None):
    conn = mappa.connect()
    tm = conn.create('http://www.semagia.com/mappa-test-tm')
    src = Source(file=open(filename, 'rb'))
    deserializer.handler = MappaMapHandler(tm)
    deserializer.parse(src)
    if post_process:
        post_process(tm)
    reference_file = os.path.abspath(os.path.dirname(filename) + '/../baseline/%s.cxtm' % os.path.basename(filename))
    expected = codecs.open(reference_file, 'r', encoding='utf-8').read()
    result = StringIO()
    c14n = CXTMTopicMapWriter(result, src.iri)
    c14n.write(tm)
    res = unicode(result.getvalue(), 'utf-8')
    if expected != res:
        fail(u'failed: %s.\nExpected: %s\nGot: %s' % (filename, expected, res))


def check_invalid(deserializer, filename):
    conn = mappa.connect()
    tm = conn.create('http://www.semagia.com/mappa-test-tm')
    src = Source(file=open(filename, 'rb'))
    deserializer.handler = MappaMapHandler(tm)
    try:
        deserializer.parse(src)
        fail('Expected an error in "%s"' % filename)
    except MIOException:
        pass
    except ModelConstraintViolation:
        pass
