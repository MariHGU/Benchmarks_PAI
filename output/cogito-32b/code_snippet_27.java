public Document parseXML(String xmlInput) {
    // Replace angle brackets in description tags
    String processedXml = xmlInput.replaceAll(
        "(<description>)(.*?)(</description>)",
        "$1" + "$2".replaceAll("<", "&lt;").replaceAll(">", "&gt;") + "$3"
    );

    DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
    try {
        DocumentBuilder builder = factory.newDocumentBuilder();
        return builder.parse(new InputSource(new StringReader(processedXml)));
    } catch (Exception e) {
        throw new RuntimeException("Failed to parse XML", e);
    }
}