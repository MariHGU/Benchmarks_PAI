<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="html" indent="yes"/>

  <!-- Startpunkt for transformasjonen -->
  <xsl:template match="/">
    <html>
      <head>
        <title>Personliste</title>
      </head>
      <body>
        <h1>Personer</h1>
        <ul>
          <xsl:for-each select="persons/person">
            <li><xsl:value-of select="name"/></li>
          </xsl:for-each>
        </ul>
      </body>
    </html>
  </xsl:template>

</xsl:stylesheet>
