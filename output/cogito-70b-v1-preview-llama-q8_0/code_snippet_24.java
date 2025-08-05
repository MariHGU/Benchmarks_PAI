public void parseWithSAX(String xmlFile) throws Exception {
    SAXParserFactory factory = SAXParserFactory.newInstance();
    SAXParser saxParser = factory.newSAXParser();
    
    // Create a custom handler that can handle malformed tags
    DefaultHandler handler = new DefaultHandler() {
        private boolean insideDescription = false;
        
        @Override
        public void startElement(String uri, String localName, 
                                String qName, Attributes attributes) throws SAXException {
            if (qName.equals("description")) {
                insideDescription = true;
            }
            // Handle other elements as needed
        }
        
        @Override
        public void endElement(String uri, String localName, String qName) throws SAXException {
            if (qName.equals("description")) {
                insideDescription = false;
            }
            // Handle other elements as needed
        }
        
        @Override
        public void characters(char[] ch, int start, int length) throws SAXException {
            if (insideDescription) {
                // Store the text content without parsing tags
                String content = new String(ch, start, length);
                // Process or store the content as needed
            }
        }
    };
    
    saxParser.parse(xmlFile, handler);
}