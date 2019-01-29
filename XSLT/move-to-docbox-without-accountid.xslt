<?xml version="1.0"?>
<!--This XSLT can be used when a jdf ticket only contains the media name and not the other attributes that are needed by PRISMAsync.
    For this xslt to work correctly the names in the PRISMAsync media catalog need to be unique.
    For all media used in jobs send a match needs to be added to replace 
    It matches Medianame and replaces the complete element keeping the .
-->
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:oce="http://www.oce.com/JDF_Extension/1_00"
                xmlns="http://www.CIP4.org/JDFSchema_1_1"
                xmlns:jdfns="http://www.CIP4.org/JDFSchema_1_1" exclude-result-prefixes="jdfns">
  <xsl:output method="xml" encoding="utf-8" indent="no"/>

  <!-- Define MediaDescriptiveName to be able to use it in a statement later on -->
  <xsl:variable name="MediaDescriptiveName"
     select="//jdfns:ResourcePool//jdfns:Media/@DescriptiveName"/>

  <!-- Define MediaId to keep it for replacing the media entry and making sure it still links to the ResourceLinkPool-->
  <xsl:variable name="MediaID"
     select="//jdfns:ResourcePool//jdfns:Media/@ID"/>

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
  <xsl:template match="jdfns:JDF/jdfns:ResourcePool/jdfns:Media">
    <!--If different jobs contain different media: repeat the if statement below for eacht used media (or copy this complete xslt-->
    <xsl:if test= "contains($MediaDescriptiveName,'My Media description')">
      <Media ID="{$MediaID}" Class="Consumable" DescriptiveName="My Media description" Dimension="595.27559055 841.88976378" Status="Available" Thickness="102" Weight="150" MediaColorName="White" HoleType="None" MediaSetCount="1" MediaType="Paper" MediaTypeDetails="TopColor" oce:CustomMediaType="TopColor">
      </Media>
    </xsl:if>
  </xsl:template>

</xsl:stylesheet>