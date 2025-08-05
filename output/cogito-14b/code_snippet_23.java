DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setEntityResolver(new EntityResolver() {
    @Override
    public InputSource resolveEntity(String publicId, String systemId) throws SAXException, IOException {
        // Return null to prevent the parser from trying to expand entities
        return new InputSource(new StringReader(""));
    }
});