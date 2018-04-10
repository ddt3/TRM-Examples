<?xml version="1.0"?>
<!--This XSLT will add 2 staples to a job if the JobName contains "_2staple"

    It matches CustomerJobname and will add a StitchingParams if CustomerJobName contains _2staple .
    It matches CustomerInfoLink and will add a StitchingParamsLink if CustomerJobName contains _2staple.
-->
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:oce="http://www.oce.com/JDF_Extension/1_00"
                xmlns="http://www.CIP4.org/JDFSchema_1_1"
                xmlns:jdfns="http://www.CIP4.org/JDFSchema_1_1" exclude-result-prefixes="jdfns">
  <xsl:output method="xml" encoding="utf-8" indent="no"/>
  
  <!-- Define jobName to be able to use it in a statement later on -->
  <xsl:variable name="jobName"
     select="//jdfns:ResourcePool//CustomerInfo/@CustomerJobName"/>

  <!-- In xslt finding a match does not automatically mean: copy the contents 
   This snippet in the script matches anything and copies it to the output, to make sure the whole ticket is copied to the output
   
   Priority of this match is: -.5
   -->
  
  <xsl:template match="@*|node()|comment()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()|comment()"/>
    </xsl:copy>
  </xsl:template>
  <!--Match on CustomerInfo, the JDF node that contains the Jobname property 
  
      Priority of this match is: .5
  -->
  <xsl:template match="jdfns:JDF/jdfns:ResourcePool/CustomerInfo">
    <xsl:copy-of select="."/>

    <xsl:if test= "contains( $jobName,'_2staple')">
      <xsl:text>&#xa;</xsl:text>
<!--If jobName contains _staple-->

      <StitchingParams ID="Sample_Jobname_to_stapling-Solution-2.xslt" Class="Parameter" NumberOfStitches="2" Status="Available" StitchType="Side" />
    </xsl:if>
  </xsl:template>

  <xsl:template match="jdfns:JDF/jdfns:ResourceLinkPool/jdfns:CustomerInfoLink">
    <xsl:copy-of select="."/>

    <xsl:if test= "contains( $jobName,'_2staple')">
      <xsl:text>&#xa;</xsl:text>
      <StitchingParamsLink Usage="Input" rRef="Sample_Jobname_to_stapling-Solution-2.xslt"/>
    </xsl:if>
  </xsl:template>

</xsl:stylesheet>