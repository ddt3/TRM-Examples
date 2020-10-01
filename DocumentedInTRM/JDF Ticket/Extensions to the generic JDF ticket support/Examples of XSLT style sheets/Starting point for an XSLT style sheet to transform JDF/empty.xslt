<?xml version="1.0"?>
<!--This XSLT can be used as a starting point to transform JDF
    The result of the transform done with this xslt is a simple matching of all elements of the JDF ticket and copying it to the output ticket.
    So this XSLT is a simple transformation which copies input ticket to the output ticket. 

    This XSLT uses a namespace called jdfns to refer to xml elements from JDFSchema_1_1 namespace.
-->
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:oce="http://www.oce.com/JDF_Extension/1_00"
                xmlns="http://www.CIP4.org/JDFSchema_1_1"
                xmlns:jdfns="http://www.CIP4.org/JDFSchema_1_1" exclude-result-prefixes="jdfns">
  <xsl:output method="xml" encoding="utf-8" indent="no"/>
  
 
   <!--
   This snippet in the script matches anything and copies it to the output, to make sure the whole ticket is copied to the output 
    -->
   <xsl:template match="@*|node()|comment()">
    <xsl:copy> <!--In xslt finding a match does not automatically mean copy the contents. So we explicitly copy here -->
      <xsl:apply-templates select="@*|node()|comment()"/>
    </xsl:copy>
  </xsl:template>
  
</xsl:stylesheet>
