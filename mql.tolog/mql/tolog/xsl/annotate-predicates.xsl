<?xml version="1.0" encoding="utf-8"?>
<!--
  This stylesheet annotates predicates like "type" and "value" with
  a "hint" attribute that indicates which kind of Topic Maps statement
  is meant.
  
  I.e.:
    
    association($a), type($a, $type)?

    Input XML:
      <builtin-predicate name="asssociation">
        [...]
      </builtin-predicate>
      <builtin-predicate name="type">
         [...]
      </builtin-predicate>

    Output XML:
      <builtin-predicate name="asssociation">
        [...]
      </builtin-predicate>
      <builtin-predicate name="type" association="true">
        [...]
      </builtin-predicate>

  
  Supported predicates:
  * type
  * scope
  * value
  * value-like
  * datatype
  * reifies

  Copyright (c) 2010 - 2011, Semagia - Lars Heuer <http://www.semagia.com/>
  All rights reserved.
  
  License: BSD
-->
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tl="http://psi.semagia.com/tolog-xml/"
                xmlns="http://psi.semagia.com/tolog-xml/"
                exclude-result-prefixes="tl">

  <xsl:output method="xml" encoding="utf-8" standalone="yes"/>

  <xsl:key name="assocs" 
            match="tl:builtin-predicate[@name='association' or @name='association-role']/tl:*[1][local-name(.) = 'variable']" 
            use="@name"/>

  <xsl:key name="roles" 
            match="tl:builtin-predicate[@name='association-role']/tl:*[2][local-name(.) = 'variable']" 
            use="@name"/>

  <xsl:key name="occs" 
            match="tl:builtin-predicate[@name='occurrence']/tl:*[2][local-name(.) = 'variable']"
            use="@name"/>

  <xsl:key name="names" 
            match="tl:builtin-predicate[@name='topic-name']/tl:*[2][local-name(.) = 'variable']|tl:builtin-predicate[@name='variant']/tl:*[1][local-name(.) = 'variable']"
            use="@name"/>

  <xsl:key name="variants"
            match="tl:builtin-predicate[@name='variant']/tl:*[2][local-name(.) = 'variable']"
            use="@name"/>


  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='type' 
                                            or @name='scope' 
                                            or @name='value'
                                            or @name='value-like'
                                            or @name='datatype'][tl:*[1][local-name(.)='variable']]">
    <xsl:call-template name="annotate"/>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='reifies'][tl:*[2][local-name(.)='variable']]">
    <xsl:call-template name="annotate">
      <xsl:with-param name="index" select="2"/>
    </xsl:call-template>
  </xsl:template>


  <xsl:template name="annotate">
    <xsl:param name="index" select="1"/>
    <xsl:variable name="key" select="tl:*[$index][local-name(.) = 'variable']/@name"/>
    <builtin-predicate>
      <xsl:copy-of select="@*"/>
      <xsl:if test="key('assocs', $key)">
        <xsl:attribute name="association"><xsl:text>true</xsl:text></xsl:attribute>
      </xsl:if>
      <xsl:if test="key('roles', $key)">
        <xsl:attribute name="role"><xsl:text>true</xsl:text></xsl:attribute>
      </xsl:if>
      <xsl:if test="key('occs', $key)">
        <xsl:attribute name="occurrence"><xsl:text>true</xsl:text></xsl:attribute>
      </xsl:if>
      <xsl:if test="key('names', $key)">
        <xsl:attribute name="topic-name"><xsl:text>true</xsl:text></xsl:attribute>
      </xsl:if>
      <xsl:if test="key('variants', $key)">
        <xsl:attribute name="variant"><xsl:text>true</xsl:text></xsl:attribute>
      </xsl:if>
      <xsl:copy-of select="*"/>
    </builtin-predicate>
  </xsl:template>

</xsl:stylesheet>