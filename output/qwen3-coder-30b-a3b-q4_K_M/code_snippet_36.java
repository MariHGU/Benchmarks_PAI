public Document parseWithRecovery(String xmlString) throws Exception {
    // First, try to parse normally
    try {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        return builder.parse(new ByteArrayInputStream(xmlString.getBytes("UTF-8")));
    } catch (Exception e) {
        // If that fails, attempt recovery
        String fixedXml = fixInvalidXml(xmlString);
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        return builder.parse(new ByteArrayInputStream(fixedXml.getBytes("UTF-8")));
    }
}

private String fixInvalidXml(String xml) {
    // Replace problematic content with escaped versions
    // This is a more comprehensive approach for your specific case
    return xml.replaceAll(
        "<description>([^<]*?)<([^>]*?)>([^<]*?)</description>",
        "<description>$1&amp;lt;$2&amp;gt;$3</description>"
    );
}