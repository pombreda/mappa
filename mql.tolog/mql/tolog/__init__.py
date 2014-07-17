# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Provides functions to parse tolog queries.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from __future__ import absolute_import
from functools import partial
from urllib2 import urlopen
import lxml.sax #TODO: Any chance to remove this dependency (here)?
from tm import Source, plyutils, xmlutils
from . import handler as handler_mod, xsl

__all__ = ('parse', 'parse_query')


def parse(src, handler, tolog_plus=False, **kw):
    """\
    Parses the provided query and issues events against the provided handler.
    
    `src`
        A string, a file object or a `tm.Source` instance to read the query from.
        If a string is used, this function expects an iri keyword which
        defines the base IRI.
    `handler`
        A `ITologHandler` which receives the events generated by the parser.
    `tolog_plus`
        Indicates if tolog+ parsing mode should be enabled.
        Note: If the query starts with a ``%version`` directive, the 
        tolog+ mode is enabled automatically, regardless of the provided
        `tolog_plus` value
    """
    from mql.tolog import parser as parser_mod
    parser = plyutils.make_parser(parser_mod)
    parser_mod.initialize_parser(parser, handler, tolog_plus)
    if isinstance(src, basestring):
        iri = kw.get('iri')
        if not iri:
            raise ValueError('If the query source is a string, an "iri" keyword is expected')
        src = Source(data=src, iri=iri)
    elif isinstance(src, file):
        src = Source(file=src, iri=kw.get('iri'))
    data = src.stream or urlopen(src.iri)
    handler.base_iri = src.iri
    handler.start()
    lexer = _make_lexer(tolog_plus)
    parser.parse(data.read(), lexer=lexer)
    handler.end()


def _make_lexer(tolog_plus):
    """\
    Creates and returns the lexer.

    `tolog_plus`
        Indicates if the lexer should read tolog+.
        (Even if this parameter is ``False``, the lexer may switch to
        tolog+-mode iff a %version directive is found).
    """
    from mql.tolog import lexer as lexer_mod
    lexer = plyutils.make_lexer(lexer_mod)
    lexer.tolog_plus = tolog_plus
    return lexer


def parse_query(src, query_handler=None, factory=None, tolog_plus=False, optimizers=None, **kw):
    """\
    Parses and optimizes the query and returns an executable query.
    
    If the `handler` is ``None`` and the ``factory`` is ``None`` a default
    handler/factory combination will be used. If the handler is not ``None``,
    the factory argument will be ignored. If the `factory` is provided and
    the `handler` is ``None``, a default handler will be used which utilizes
    the provided factory to create the query.
    
    `src`
        A string, a file object or a `tm.Source` instance to read the query from.
        If a string is used, this function expects an iri keyword which
        defines the base IRI.
    `query_handler`
        A `IQueryHandler` which receives events to construct a query
    `factory`
        A `IQueryFactory` which is used to construct the query.
    `tolog_plus`
        Indicates if tolog+ parsing mode should be enabled.
        Note: If the query starts with a ``%version`` directive, the 
        tolog+ mode is enabled automatically, regardless of the provided
        `tolog_plus` value
    `optimizers`
        An optional iterable of optimizer names which should be applied to
        the parsed provided query. If the optimizers are not provided,
        a default set of optimizers will be applied to the query.
        To omit any optimization, an empty iterable must be provided.
    """
    query_handler = query_handler or handler_mod.make_queryhandler(factory)
    query_handler.base_iri = src.iri
    if optimizers is None:
        optimizers = xsl.DEFAULT_TRANSFORMERS
    xsl.apply_transformations(parse_to_etree(src, tolog_plus, **kw), optimizers,
                              partial(xsl.saxify, handler=handler_mod.XMLParserHandler(query_handler)))
    return query_handler.query


def parse_to_etree(src, tolog_plus=False, **kw):
    """\
    Returns the provided query as Etree.
    
    `src`
        A string, a file object or a `tm.Source` instance to read the query from.
        If a string is used, this function expects an iri keyword which
        defines the base IRI.
    `tolog_plus`
        Indicates if tolog+ parsing mode should be enabled.
        Note: If the query starts with a ``%version`` directive, the 
        tolog+ mode is enabled automatically, regardless of the provided
        `tolog_plus` value
    """
    contenthandler = lxml.sax.ElementTreeContentHandler()
    parse(src, handler_mod.XMLParserHandler(xmlutils.SAXSimpleXMLWriter(contenthandler)), tolog_plus, **kw)
    return contenthandler.etree


def parse_to_tolog(src, tolog_plus=False, hints=False, optimizers=None, **kw):
    """\
    Parses the provided query and returns the query as an optimized tolog
    query string. 
    
    This function is mainly useful for debugging purposes.
    
    `src`
        A string, a file object or a `tm.Source` instance to read the query from.
        If a string is used, this function expects an iri keyword which
        defines the base IRI.
    `tolog_plus`
        Indicates if tolog+ parsing mode should be enabled.
        Note: If the query starts with a ``%version`` directive, the 
        tolog+ mode is enabled automatically, regardless of the provided
        `tolog_plus` value
    `hints`
        Indicates if the resulting tolog query string should contain hints
        which are inserted by the query optimizer (disabled by default).
    `optimizers`
        An optional iterable of optimizer names which should be applied to
        the parsed provided query. If the optimizers are not provided,
        a default set of optimizers will be applied to the query.
        To omit any optimization, an empty iterable must be provided.
    """
    return _back_to_tolog(src, False, tolog_plus=tolog_plus, hints=hints,
                          optimizers=optimizers, **kw)
    

def parse_to_tologplus(src, tolog_plus=False, hints=False, optimizers=None, **kw):
    """\
    Parses the provided query and returns the query as an optimized tolog+
    query string. 
    
    `src`
        A string, a file object or a `tm.Source` instance to read the query from.
        If a string is used, this function expects an iri keyword which
        defines the base IRI.
    `tolog_plus`
        Indicates if tolog+ parsing mode should be enabled.
        Note: If the query starts with a ``%version`` directive, the 
        tolog+ mode is enabled automatically, regardless of the provided
        `tolog_plus` value
    `hints`
        Indicates if the resulting tolog query string should contain hints
        which are inserted by the query optimizer (disabled by default).
    `optimizers`
        An optional iterable of optimizer names which should be applied to
        the parsed provided query. If the optimizers are not provided,
        a default set of optimizers will be applied to the query.
        To omit any optimization, an empty iterable must be provided.
    """
    return _back_to_tolog(src, True, tolog_plus=tolog_plus, hints=hints,
                          optimizers=optimizers)


def _back_to_tolog(src, tolog_plus_out, tolog_plus=False, hints=False, optimizers=None, **kw):
    """\
    Parses the provided query and returns the query as an optimized tolog(+)
    query string. 
    
    `src`
        A string, a file object or a `tm.Source` instance to read the query from.
        If a string is used, this function expects an iri keyword which
        defines the base IRI.
    `tolog_plus_out`
        Indicates if the resulting query should use tolog+ syntax.
    `tolog_plus`
        Indicates if tolog+ parsing mode should be enabled.
        Note: If the query starts with a ``%version`` directive, the 
        tolog+ mode is enabled automatically, regardless of the provided
        `tolog_plus` value
    `hints`
        Indicates if the resulting tolog query string should contain hints
        which are inserted by the query optimizer (disabled by default).
    `optimizers`
        An optional iterable of optimizer names which should be applied to
        the parsed provided query. If the optimizers are not provided,
        a default set of optimizers will be applied to the query.
        To omit any optimization, an empty iterable must be provided.
    """
    if optimizers is None:
        optimizers = xsl.DEFAULT_TRANSFORMERS
    transformers = tuple(optimizers) + ('back-to-tolog',)
    transform_kw = {'render-hints': '"true"' if hints else '"false"',
                    'tolog-plus': '"true"' if tolog_plus_out else '"false"'}
    return xsl.apply_transformations(parse_to_etree(src, tolog_plus, **kw),
                                     transformers, **transform_kw)
