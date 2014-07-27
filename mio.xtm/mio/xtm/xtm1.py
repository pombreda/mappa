# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
This module provides classes to read 
`XML Topic Maps (XTM) 1.0 <http://www.topicmaps.org/xtm/1.0/>`_

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
import xml.sax as sax
import xml.sax.handler as sax_handler
from tm import TMDM, XSD, XTM_10, mio, voc
from tm.mio.deserializer import Context
from tm.irilib import resolve_iri

__all__ = ['XTM10ContentHandler']

# XML namespace
NS_XML = u'http://www.w3.org/XML/1998/namespace'

# XTM 1.0 namespace
NS_XTM = voc.XTM_10

# XLink namespace
NS_XLINK = voc.XLINK


# Constants for XTM elements.
MERGE_MAP = u'mergeMap'
TOPIC_MAP = u'topicMap'
TOPIC = u'topic'
ASSOCIATION = u'association'
MEMBER = u'member'
ROLE_SPEC = u'roleSpec'
OCCURRENCE = u'occurrence'
BASE_NAME = u'baseName'
BASE_NAME_STRING = u'baseNameString'
VARIANT = u'variant'
VARIANT_NAME = u'variantName'

INSTANCE_OF = u'instanceOf'

RESOURCE_REF = u'resourceRef'
RESOURCE_DATA = u'resourceData'

SCOPE = u'scope'
PARAMETERS = u'parameters'

TOPIC_REF = u'topicRef'

SUBJECT_IDENTITY = u'subjectIdentity'
SUBJECT_INDICATOR_REF = u'subjectIndicatorRef'

#pylint: disable-msg=E1103
class XTM10ContentHandler(object, sax_handler.ContentHandler):
    """\
    XTM 1.0 content handler.

    .. Note::
        
       This content handler does not support more than one topic map in
       an XTM file.
    """
    _ASSOCIATION = mio.SUBJECT_IDENTIFIER, XTM_10.DEFAULT_ASSOCIATION_TYPE
    _ROLE = mio.SUBJECT_IDENTIFIER, XTM_10.DEFAULT_ROLE_TYPE
    _TOPIC_NAME = mio.SUBJECT_IDENTIFIER, TMDM.topic_name
    _OCURRENCE = mio.SUBJECT_IDENTIFIER, XTM_10.DEFAULT_OCCURRENCE_TYPE

    def __init__(self, map_handler=None, locator=None):
        """\
        Initializes this handler with the specified input adapter `adapter`
        """
        self.map_handler = map_handler
        self.subordinate = False
        self.context = Context()
        self.reset(locator)
        self.strict = True

    def reset(self, locator=None):
        self._stack = []    # Stack of element names
        self._content = []
        self._accept_content = False
        self._bases = []    # Stack of base locators
        self.scope = []    # Scope which was generated by mergeMap
        self._seen_type = False
        self._seen_scope = False
        self._role_type = None
        self._variants = []
        self._mergemap = None
        if locator:
            self._bases.append(locator)

    def _get_doc_iri(self):
        if self._bases:
            return self._bases[-1]
        return None

    def _set_doc_iri(self, locator):
        self._bases.append(locator)

    def setDocumentLocator(self, locator):
        self._bases.append(locator.getSystemId())

    def startElementNS(self, (uri, name), qname, attrs):
        if uri != NS_XTM and uri != u'':
            return
        handler = self.map_handler
        stack = self._stack
        href = self._href
        create_locator = self._create_locator
        process_iid = self._process_iid
        base = attrs.get((None, u'base'), None) or attrs.get((NS_XML, u'base'), None)
        if base:
            base = create_locator(base)
        self._bases.append(base or self._bases[-1])
        if name in (INSTANCE_OF, SUBJECT_IDENTITY,
                    ROLE_SPEC, VARIANT_NAME, PARAMETERS):
            stack.append(name)
        elif TOPIC_REF == name:
            self._process_topic_reference_iri(href(attrs))
        elif TOPIC == name:
            handler.startTopic((mio.ITEM_IDENTIFIER, create_locator(u'#' + attrs.get((None, u'id')))))
            stack.append(TOPIC)
        elif SUBJECT_INDICATOR_REF == name:
            self._process_sid(href(attrs))
        elif RESOURCE_REF == name:
            self._process_resource_ref(href(attrs))
        elif ASSOCIATION == name:
            handler.startAssociation()
            process_iid(attrs)
            stack.append(ASSOCIATION)
            self._seen_scope = False
            self._seen_type = False
        elif MEMBER == name:
            self._role_type = None
            stack.append(MEMBER)
        elif OCCURRENCE == name:
            handler.startOccurrence()
            process_iid(attrs)
            stack.append(OCCURRENCE)
            self._seen_scope = False
            self._seen_type = False
        elif BASE_NAME == name:
            handler.startName()
            process_iid(attrs)
            stack.append(BASE_NAME)
            self._seen_scope = False
            self._seen_type = False
        elif name in (BASE_NAME_STRING, RESOURCE_DATA):
            self._content = []
            self._accept_content = True
        elif VARIANT == name:
            iid = attrs.get((None, u'id'), None)
            if iid:
                iid = create_locator(u'#' + iid)
            variant = Variant(iid)
            # Inherit the scope from the variant's parents
            for v in self._variants:
                variant.scope.extend(v.scope)
            self._variants.append(variant)
            self._seen_scope = False
        elif SCOPE == name:
            handler.startScope()
            self._seen_scope = True
            self._process_mergemap_themes()
            stack.append(SCOPE)
        elif TOPIC_MAP == name:
            stack.append(TOPIC_MAP)
            process_iid(attrs)
        elif MERGE_MAP == name:
            self._mergemap = MergeMap(href(attrs))
            stack.append(MERGE_MAP)
        else:
            raise mio.MIOException('Unknown start element "%s"' % name)

    def endElementNS(self, (uri, name), qname):
        if uri != NS_XTM and uri != u'':
            return
        stack = self._stack
        handler = self.map_handler
        if name in (INSTANCE_OF, SUBJECT_IDENTITY, TOPIC_MAP,
                    VARIANT_NAME, PARAMETERS, ROLE_SPEC, MEMBER):
            stack.pop()
        elif TOPIC == name:
            handler.endTopic()
            stack.pop()
        elif ASSOCIATION == name:
            stack.pop()
            if not self._seen_type:
                handler.type(XTM10ContentHandler._ASSOCIATION)
            self._process_mergemap_scope()
            handler.endAssociation()
        elif OCCURRENCE == name:
            stack.pop()
            if not self._seen_type:
                handler.type(XTM10ContentHandler._OCURRENCE)
            self._process_mergemap_scope()
            handler.endOccurrence()
        elif BASE_NAME == name:
            stack.pop()
            if not self._seen_type:
                handler.type(XTM10ContentHandler._TOPIC_NAME)
            self._process_mergemap_scope()
            handler.endName()
        elif BASE_NAME_STRING == name:
            handler.value(u''.join(self._content))
            self._accept_content = False
        elif RESOURCE_DATA == name:
            parent_el = stack[-1]
            value = u''.join(self._content), XSD.string
            if OCCURRENCE == parent_el:
                handler.value(*value)
            elif VARIANT_NAME == parent_el:
                self._variants[-1].literal = value
            else:
                raise mio.MIOException('Unexpected parent element "%s" while processing "resourceData"' % parent_el)
            self._accept_content = False
        elif VARIANT == name:
            variant = self._variants.pop()
            if not variant.seen_scope:
                raise mio.MIOException('The variant "%s" has no scope' % variant)
            handler.startVariant()
            handler.startScope()
            for theme in variant.scope:
                handler.theme(theme)
            self._process_mergemap_themes()
            handler.endScope()
            if variant.iid:
                handler.itemIdentifier(variant.iid)
            handler.value(*variant.literal)
            handler.endVariant();
        elif MERGE_MAP == name:
            if self._mergemap.iri not in self.context.loaded:
                self.context.add_loaded(self._mergemap.iri)
                self._mergemap.execute(self.map_handler, self.scope, self.context)
        elif SCOPE == name:
            stack.pop()
            handler.endScope()
        elif name in (TOPIC_REF, RESOURCE_REF, SUBJECT_INDICATOR_REF):
            pass # noop.
        else:
            raise mio.MIOException('Unknown end element "%s"' % name)

    def startDocument(self):
        pass

    def endDocument(self):
        self.reset()

    def characters(self, content):
        if self._accept_content:
            self._content.append(content)

    def _href(self, attrs):
        """\
        Returns an absolute IRI from the attributes.
        """
        return self._create_locator(attrs.get((NS_XLINK, u'href')))

    def _process_iid(self, attrs):
        iid = attrs.get((None, u'id'), None)
        if iid:
            return self.map_handler.itemIdentifier(self._create_locator(u'#%s' % iid))

    def _create_locator(self, reference):
        """\
        Returns a locator where ``reference`` is resolved against the base
        locator.
        """
        return resolve_iri(self._bases[-1], reference)

    def _process_topic_reference_iri(self, iri):
        parent_el = self._stack[-1]
        if SUBJECT_IDENTITY == parent_el:
            self.map_handler.itemIdentifier(iri)
        else:
            self._process_topic_ref(parent_el, (mio.ITEM_IDENTIFIER, iri))

    def _process_topic_ref(self, parent_el, ref):
        """\
        Processes a ``topicRef`` element in the context of ``parent_el``.
        
        `parent_el`
            The parent element.
        `ref`
            A (kind, iri) tuple
        """
        handler = self.map_handler
        if INSTANCE_OF == parent_el:
            stack = self._stack 
            if ASSOCIATION in stack or OCCURRENCE in stack:
                handler.type(ref)
                self._seen_type = True
            elif TOPIC in stack:
                handler.isa(ref)
            else:
                raise mio.MIOException('Unexpected "instanceOf" element')
        elif MEMBER == parent_el:
            if not self._role_type:
                self._role_type = ref
            handler.startRole(self._role_type)
            handler.player(ref)
            handler.endRole()
        elif SCOPE == parent_el:
            self._process_theme(ref)
        elif PARAMETERS == parent_el:
            self._variants[-1].seen_scope = True
            self._variants[-1].scope.append(ref)
        elif ROLE_SPEC == parent_el:
            self._role_type = ref
        elif MERGE_MAP == parent_el:
            self._mergemap.add_theme(ref)
        else:
            raise mio.MIOException('Unexpected parent element "%s" while processing topicRef' % parent_el)

    def _process_mergemap_scope(self):
        """\
        
        """
        if self._seen_scope or not self.scope:
            return
        self.map_handler.startScope()
        self._process_mergemap_themes()
        self.map_handler.endScope()

    def _process_mergemap_themes(self):
        """\
        
        """
        theme = self.map_handler.theme
        for theme_ref in self.scope:
            theme(theme_ref)

    def _process_role(self, player):
        """\
        Creates an association role with the specified player.
        """
        handler = self.map_handler
        handler.startRole(self._role_type or XTM10ContentHandler._ROLE)
        handler.player(player)
        handler.endRole()

    def _process_theme(self, ref):
        """\
        
        """
        stack = self._stack
        if ASSOCIATION in stack or OCCURRENCE in stack or BASE_NAME in stack:
            self.map_handler.theme(ref)
        else:
            raise mio.MIOException('Unexpected parent element while processing scope')

    def _process_sid(self, iri):
        """\
        
        """
        parent_el = self._stack[-1]
        if SUBJECT_IDENTITY == parent_el:
            self.map_handler.subjectIdentifier(iri)
        else:
            self._process_topic_ref(parent_el, (mio.SUBJECT_IDENTIFIER, iri))

    def _process_resource_ref(self, ref):
        """\
        
        """
        handler = self.map_handler
        parent_el = self._stack[-1]
        if SUBJECT_IDENTITY == parent_el:
            handler.subjectLocator(ref)
        elif OCCURRENCE == parent_el:
            handler.value(ref, XSD.anyURI)
        elif VARIANT_NAME == parent_el:
            self._variants[-1].literal = ref, XSD.anyURI
        else:
            slo = mio.SUBJECT_LOCATOR, ref
            if MEMBER == parent_el:
                self._process_role(slo)
            elif SCOPE == parent_el:
                self._process_theme(slo)
            elif MERGE_MAP == parent_el:
                self._mergemap.add_theme(slo)
            else:
                raise mio.MIOException('Unexpected parent element "%s" while processing resourceRef' % parent_el)
    
    doc_iri = property(_get_doc_iri, _set_doc_iri)

class Variant(object):
    """\
    Internally used object to keep track about variants.
    """
    __slots__ = ['iid', 'literal', 'scope', 'seen_scope']
    def __init__(self, iid=None):
        """\
        
        """
        self.iid = iid
        self.literal = None
        self.scope = []
        self.seen_scope = False

    def __str__(self):
        return 'Variant(iid=%s, literal=%s, scope=%s)' % (self.iid, self.literal, self.scope)

class MergeMap(object):
    
    def __init__(self, iri):
        self.iri = iri
        self._scope = []
    def add_theme(self, theme):
        self._scope.append(theme)
    def execute(self, map_handler, scope, context):
        parser = sax.make_parser()
        parser.setFeature(sax.handler.feature_namespaces, True)
        xtmch = XTM10ContentHandler(map_handler, self.iri)
        xtmch.subordinate = True
        xtmch.context = context
        self._scope.extend(scope)
        xtmch.scope = self._scope
        parser.setContentHandler(xtmch)
        parser.parse(self.iri)

