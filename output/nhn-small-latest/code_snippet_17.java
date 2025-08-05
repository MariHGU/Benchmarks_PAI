SAXParserFactory factory = SAXParserFactory.newInstance();
factory.setNamespaceAware(false);
SAXParser saxParser = factory.newSAXParser();
InputSource source = new InputSource(new StringReader(xmlString));
saxParser.parse(source, new DefaultHandler() {
    // Implementer hendelsesmetoder her for å hente ut informasjonen du trenger
});