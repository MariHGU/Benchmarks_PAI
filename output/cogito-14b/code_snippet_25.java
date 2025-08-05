SAXParserFactory spf = SAXParserFactory.newInstance();
spf.setNamespaceAware(true); // If you're using namespaces

XMLReader reader = spf.newSAXParser().getXMLReader();

class MyHandler extends DefaultHandler {
    @Override
    public void startElement(String uri, String localName, String qName, Attributes attributes) throws SAXException {
        if (qName.equals("description")) {
            // Start reading the content
        }
    }

    @Override
    public void characters(char[] ch, int start, int length) throws SAXException {
        String data = new String(ch, start, length);
        // Handle character data here
    }

    @Override
    public void endElement(String uri, String localName, String qName) throws SAXException {
        if (qName.equals("description")) {
            // End of description element
        }
    }
}

reader.setContentHandler(new MyHandler());
InputSource source = new InputSource(yourXmlInputStream);
reader.parse(source);