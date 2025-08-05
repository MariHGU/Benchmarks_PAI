DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
factory.setValidating(false);
factory.setNamespaceAware(true);

try {
    DocumentBuilder builder = factory.newDocumentBuilder();
    try {
        Document doc = builder.parse(new InputSource(new StringReader(xmlInput)));
    } catch (SAXException e) {
        // Handle parsing errors
    }
} catch (ParserConfigurationException e) {
    // Handle parser configuration errors
}