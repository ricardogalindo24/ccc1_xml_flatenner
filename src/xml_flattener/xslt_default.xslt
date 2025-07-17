<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="xml" indent="yes"/>
  <xsl:strip-space elements="*"/>

    <!-- xsl template designed for GEN5 Collision Files -->

  <xsl:template match="/ACES">
    <root>
      <xsl:apply-templates select="App"/>
    </root>
  </xsl:template>

  <xsl:template match="App">
    <App>
      <!-- Copy attributes -->
      <xsl:copy-of select="@*"/>
      <BaseVehicleID>
        <xsl:value-of select="BaseVehicle/@id"/>
      </BaseVehicleID>
      <xsl:copy-of select="Qty"/>
      <PartTypeID>
      <xsl:value-of select="PartType/@id"/>
      </PartTypeID>
      <PositionID>
	<xsl:value-of select="Position/@id"/>
      </PositionID>
      <xsl:copy-of select="Part"/>
      <!-- Loop over Notes and concatenate -->
      <xsl:variable name="notes">
        <xsl:for-each select="Note">
          <xsl:value-of select="."/>
          <xsl:if test="position() != last()">; </xsl:if>
        </xsl:for-each>
      </xsl:variable>

      <xsl:element name="Notes">
          <xsl:value-of select="$notes"/>
      </xsl:element>

      <!-- Loop over SpecSubtype and create columns from it -->
      <xsl:for-each select="SpecSubtype">
        <xsl:variable name="pos" select="position()" />
        <xsl:variable name="fieldName" select="normalize-space(.)"/>
        <xsl:variable name="fieldValue" select="normalize-space(../SpecText[$pos])"/>
        <xsl:element name="{translate($fieldName, ' ', '_')}">
          <xsl:value-of select="$fieldValue"/>
        </xsl:element>
      </xsl:for-each>
    </App>
  </xsl:template>
</xsl:stylesheet>
