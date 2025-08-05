String xmlInput = "<xml> ... <description>Example:Description:<THIS-IS-PART-OF-DESCRIPTION></description> ... </xml>";
String preprocessedXml = XmlPreprocessor.preprocessXml(xmlInput);

try {
    DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
    DocumentBuilder builder = factory.newDocumentBuilder();
    Document document = builder.parse(new InputSource(new StringReader(preprocessedXml)));
    // Process the parsed XML document
} catch (Exception e) {
    // Handle any parsing exceptions
}