DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
factory.setNamespaceAware(true);
factory.setValidating(false);
DocumentBuilder builder = factory.newDocumentBuilder();

// Ignore errors and warnings
builder.setErrorHandler(new ErrorHandler() {
    @Override
    public void warning(SAXParseException e) throws SAXException {}

    @Override
    public void error(SAXParseException e) throws SAXException {}

    @Override
    public void fatalError(SAXParseException e) throws SAXException {}
});

Document doc = builder.parse(inputStream);