public Document parseDescriptionXML(String xmlString) throws Exception {
    // Handle the specific case where description contains invalid tags
    String fixedXml = xmlString.replaceAll(
        "<description>([^<]*(?:<(?!/description>)[^<]*)*?)</description>",
        "<description><![CDATA[$1]]></description>"
    );
    
    DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
    DocumentBuilder builder = factory.newDocumentBuilder();
    return builder.parse(new ByteArrayInputStream(fixedXml.getBytes("UTF-8")));
}