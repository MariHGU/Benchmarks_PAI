SAXParserFactory factory = SAXParserFactory.newInstance();
SAXParser saxParser = factory.newSAXParser();

DefaultHandler handler = new DefaultHandler() {
    boolean inDescription = false;
    StringBuilder descriptionContent = new StringBuilder();
    
    @Override
    public void startElement(String uri, String localName, String qName) throws SAXException {
        if (qName.equals("description")) {
            inDescription = true;
        }
    }
    
    @Override
    public void endElement(String uri, String localName, String qName) throws SAXException {
        if (qName.equals("description")) {
            // Handle the collected description content here
            System.out.println(descriptionContent.toString());
            inDescription = false;
            descriptionContent.setLength(0);
        }
    }
    
    @Override
    public void characters(char[] ch, int start, int length) throws SAXException {
        if (inDescription) {
            // Collect all characters within description, ignoring nested tags
            descriptionContent.append(ch, start, length);
        }
    }
};

saxParser.parse(new InputSource(new StringReader(invalidXml)), handler);