public class CustomSAXHandler extends DefaultHandler {
    private StringBuilder currentText = new StringBuilder();
    
    @Override
    public void startElement(String uri, String localName, String qName, Attributes attributes) throws SAXException {
        if (qName.equals("THIS-IS-PART-OF-DESCRIPTION")) {
            // Handle as text content instead of a tag
            currentText.append("<THIS-IS-PART-OF-DESCRIPTION>");
        }
    }

    @Override
    public void characters(char[] ch, int start, int length) throws SAXException {
        currentText.append(new String(ch, start, length));
    }
}

// Usage:
SAXParserFactory factory = SAXParserFactory.newInstance();
factory.setValidating(false);
factory.setNamespaceAware(true);

SAXParser parser = factory.newSAXParser();

try (InputStream in = new ByteArrayInputStream(xml.getBytes())) {
    parser.parse(in, new CustomSAXHandler());
}