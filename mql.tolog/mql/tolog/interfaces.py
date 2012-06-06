# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 - 2012 -- Lars Heuer - Semagia <http://www.semagia.com/>.
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
#     * Neither the project name nor the names of the contributors may be 
#       used to endorse or promote products derived from this software 
#       without specific prior written permission.
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
Interfaces used to build a tolog query.


:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from tm.proto import Interface, Attribute

class ITologHandler(Interface):
    """\
    Common superclass of tolog query handlers.    
    """

    def start():
        """\
        The very first event.
        """

    def end():
        """\
        The last event.
        """

    def startSelect():
        """\
        Indicates the start of a SELECT statement.
        """

    def endSelect():
        """\
        Indicates the end of a SELECT statement.
        """

    def startInsert():
        """\
        Indicates the start of an INSERT statement.
        """

    def endInsert():
        """\
        Indicates the end of an INSERT statement.
        """

    def startDelete():
        """\
        Indicates the start of a DELETE statement.
        """

    def endDelete():
        """\
        Indicates the end of a DELETE statement.
        """

    def startMerge():
        """\
        Indicates the start of a MERGE statement.
        """

    def endMerge():
        """\
        Indicates the end of a MERGE statement.
        """

    def startUpdate():
        """\
        Indicates the start of an UPDATE statement.
        """

    def endUpdate():
        """\
        Indicates the end of an UPDATE statement.
        """

    def startWhere():
        """\
        Indicates the start of the WHERE clause.
        """

    def endWhere():
        """\
        Indicates the end of the WHERE clause.
        """

    def startRule(name):
        """\
        Indicates the start of a rule definition.
        
        Subsequent events define the variables in the rule's header followed
        by a `startBody` event.
        
        `name`
            Name of the rule.
        """

    def endRule():
        """\
        Indicates the end of a rule defintion.
        """

    def startBody():
        """\
        Indicates the start of a rule body definition.
        
        Subsequent events define the clauses of the rule body.
        """

    def endBody():
        """\
        Indicates the end of a rule body definition.
        """

    def base(iri):
        """\
        
        `iri`
            The base IRI all IRIs should be resolved against.
        """

    def namespace(identifier, iri, kind):
        """\
        
        `identifier` 
            The identifier to which the IRI is assigned to.
        `iri`
            The IRI.
        """

    def startBuiltinPredicate(name, hints=None):
        """\
        Indicates the start of a built-in predicate.
        
        `name`
            Name of the predicate.
        `hints`
            An optional iterable of strings indicating the type of 
            the Topic Maps construct.
            
                association
                role
                occurrence
                name
                variant
        """

    def endBuiltinPredicate():
        """\
        Indicates the end of a built-in predicate.        
        """

    def startInternalPredicate(name, hints=None, removed_variables=None):
        """\
        Indicates the start of an internal predicate.
        
        If internal predicates aren't supported, it is possible to reconstruct
        the built-in predicate. I.e. if the internal predicate is ``types($x)``,
        the handler may construct the built-in predicate 
        ``instance-of(removed_variables[0], $x)``

        `name`
            Name of the predicate.
        `hints`
            An optional iterable of strings indicating the type of 
            the Topic Maps construct.
            
                association
                role
                occurrence
                name
                variant
        `removed_variables`
            An optional iterable of strings containing the removed variable
            names.
        """

    def endInternalPredicate():
        """\
        Indicates the end of an internal predicate.
        """

    def startInfixPredicate(name):
        """\
        Indictaes the start of an infix predicate definition.
        
        The subsequent events indicate the left hand side and then the 
        right hand side of the expression.
        
        `name`
            The name of the predicate: ``eq`` (``=``), ``ne`` (``/=``), 
            ``lt`` (``<``), ``le`` (``<=``), ``gt`` (``>``), ``ge`` (``>=``).
        """

    def endInfixPredicate():
        """\
        Indictaes the end of an infix predicate definition.
        """

    def startAssociationPredicate():
        """\
        Indictaes the start of an association predicate definition.
        """

    def endAssociationPredicate():
        """\
        Indictaes the end of an association predicate definition.
        """

    def startPair():
        """\
        Indicates the start of a type: player pair
        """

    def endPair():
        """\
        Indicates the end of a type: player pair.
        """

    def startType():
        """\
        Indicates the start of a type.
        """

    def endType():
        """\
        Indicates the end of a type.
        """

    def startPlayer():
        """\
        Indicates the start of a player.
        """

    def endPlayer():
        """\
        Indicates the end of a player.
        """

    def startDynamicPredicate():
        """\
        Indictaes the start of a dynamic predicate definition.
        """

    def endDynamicPredicate():
        """\
        Indictaes the end of a dynamic predicate definition.
        """

    def startPredicate():
        """\
        Indictaes the start of a rule or module function invocation.
        """

    def endPredicate():
        """\
        Indictaes the end of a rule or module function invocation.
        """

    def startName():
        """\
        Indictaes the start of predicate, association predicate, or dynamic 
        predicate name definition.
        """

    def endName():
        """\
        Indictaes the end of predicate, association predicate, or dynamic 
        predicate name definition.
        """

    def startFragment():
        """\
        Indicates the start of a fragment.
        
        Subsequent events define the variables used within the fragment (if any)
        followed by a ``fragmentContent`` event.
        """

    def endFragment():
        """\
        Indicates the end of a fragment.
        """

    def fragmentContent(content):
        """\
        Reports the fragment's content.
        
        `content`
            A string representing the fragment.
        """

    def startNot():
        """\
        Indicates the start of a Not clause.
        """

    def endNot():
        """\
        Indicates the end of a Not clause.
        """

    def startOr():
        """\
        Indicates the start of an Or expression.
        """

    def endOr():
        """\
        Indicates the end of an Or expression.
        """

    def startBranch(short_circuit=False):
        """\
        Starts an Or-branch.
        
        `short_circuit`
            Indicates if the branch should be evaluated only if the first
            branch returns false (iff ``short_circuit`` is ``True``) or
            if this branch is evaluated in any case (``short_circuit`` is ``False``)
        """

    def endBranch():
        """\
        Indicates the end of an Or-branch.
        """

    def count(name):
        """\
        
        `name`
            Name of the variable to count (without ``$`` prefix)
        """

    def variable(name):
        """\
        
        `name`
            Name of the variable (without ``$`` prefix)
        """

    def identifier(value):
        """\
        
        `value`
            Name of the identifier.
        """

    def subjectidentifier(value):
        """\
        
        `value`
            An IRI.
        """

    def subjectlocator(value):
        """\
        
        `value`
            An IRI.
        """

    def itemidentifier(value):
        """\
        
        `value`
            An IRI.
        """

    def integer(value):
        """\
        
        `value`

        """

    def decimal(value):
        """\
        
        `value`
            
        """

    def date(value):
        """\
        
        `value`
            
        """
        
    def datetime(value):
        """\
        
        `value`
            
        """

    def iri(value):
        """\
        
        `value` 
            
        """
        
    def curie(kind, prefix, localpart):
        """\
        Reports a `CURIE <http://www.w3.org/TR/2010/NOTE-curie-20101216/>`

        `kind`
            consts.IID, consts.SID, or consts.SLO
        `prefix`
            An identifier which was previously reported via `namespace`.
        `localpart`
            Local part of the CURIE.
        """
        
    def qname(kind, prefix, localpart):
        """\
        Reports a QName.
        
        `kind`
            consts.IID, consts.SID, or consts.SLO
        `prefix`
            An identifier which was previously reported via `namespace`.
        `localpart`
            Local part of the QName.
        """

    def string(value):
        """\
        
        `value`
            
        """


class IQueryHandler(ITologHandler):
    """\
    A `ITologHandler` which provides a `query` property to retrieve the
    created query.
    """
    query = Attribute("""\
A query object.

This may be ``None`` until the `end` method was invoked.
""")


class IQueryFactory(Interface):
    """\
    
    """
    def create_select_query(header, where, order_by=None, limit=None, offset=None):
        """\
        
        """

    def create_insert_query(variables, fragment, where, order_by=None, limit=None, offset=None):
        """\
        
        """

    def create_merge_query(variables, where, order_by=None, limit=None, offset=None):
        """\
        
        """

    def create_update_query(where, order_by=None, limit=None, offset=None):
        """\
        
        """

    def create_delete_query(where, order_by=None, limit=None, offset=None):
        """\
        
        """

    def create_rule(name, args, body):
        """\
        
        `name`
            Name of the rule.
        `args`
            An iterable of variables
        `body`
            An iterable of predicates, built-in predicates, infix predicates etc.
        """

    def create_predicate(name, args):
        """\
        
        `name`
            Name of the predicate.
        `args`
            Arguments of the predicate.
        """

    def create_builtin_predicate(name, args, hints=None):
        """\
        
        `name`
            Name of the predicate.
        `args`
            Arguments of the predicate.
        `hints`
            An optional iterable of strings which name the kind of Topic Maps
            constructs are involved:
                * association
                * role
                * occurrence
                * name
                * variant
        """

    def create_internal_predicate(name, args, hints=None):
        """\
        
        `name`
            Name of the predicate.
        `args`
            Arguments of the predicate.
        `hints`
            An optional iterable of strings which name the kind of Topic Maps
            constructs are involved:
                * association
                * role
                * occurrence
                * name
                * variant
        """

    def create_infix_predicate(name, lh, rh, hints=None):
        """\
        
        `name`
            Name of the infix predicate.
        `lh`
            Left hand expression.
        `rh`
            Right hand expression.
        `hints`
            An optional iterable of strings which name the kind of Topic Maps
            constructs are involved:
                * association
                * role
                * occurrence
                * name
                * variant
        """

    def create_association_predicate(type, roles):
        """\
        
        `type`
            The association type
        `roles` 
            An iterable of (type, player) pairs.
        """

    def create_dynamic_predicate(type, topic, value):
        """\
        
        `type`
            The occurrence type.
        `topic`
            The occurrence parent.
        `value`
            The value of the occurrence.
        """

    def create_not(clauses):
        """\
        Creates a not statement.
        
        `clauses`
            An iterable of predicates, association predicates etc.
        """

    def create_or(branches, short_circuit=False):
        """\
        
        `branches`
            An iterable of clause iterables.
        """

    def create_count(variable):
        """\
        Creates a count clause.
        
        `variable`
            The variable name to count (without ``$`` prefix).
        """

    def create_iri(iri):
        """\
        Creates an IRI.
        
        `iri`
            A string representing an absolute IRI.
        """

    def resolve_iri(base, reference):
        """\
        Resolves the specified `reference` against the `base`.
        
        `base`
            An object created by `create_iri`
        `reference`
            A string representing an IRI.
        """
