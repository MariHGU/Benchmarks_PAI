DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
factory.setValidating(false); // Turn off validation
factory.setNamespaceAware(true);

// Create a new DocumentBuilder
DocumentBuilder builder = factory.newDocumentBuilder();

// Parse the input with error handling
try {
    Document doc = builder.parse(new InputSource(new StringReader(xmlInput)));
} catch (SAXException e) {
    // Handle the parsing error
}