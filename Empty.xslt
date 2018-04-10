<?xml version="1.0"?>
<!--This XSLT can be used as a starting point for a xslt to transform JDF
    It defines a namespace called jdfns. It has does no transformations it just copies input to output.
-->
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:oce="http://www.oce.com/JDF_Extension/1_00"
                xmlns="http://www.CIP4.org/JDFSchema_1_1"
                xmlns:jdfns="http://www.CIP4.org/JDFSchema_1_1" exclude-result-prefixes="jdfns">
  <xsl:output method="xml" encoding="utf-8" indent="no"/>
  
|
  <!-- In xslt finding a match does not automatically mean: copy the contents 
   This snippet in the script matches anything and copies it to the output, to make sure the whole ticket is copied to the output
   
   Priority of this match is: -.5
   -->
  
  <xsl:template match="@*|node()|comment()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()|comment()"/>
    </xsl:copy>
  </xsl:template>
  
</xsl:stylesheet>