ErrorHandler errorHandler = new ErrorHandler() {
    @Override
    public void warning(SAXParseException e) throws SAXException {
        // Handle warnings
    }

    @Override
    public void error(SAXParseException e) throws SAXException {
        // Ignore certain types of errors or handle them gracefully
        if (!e.getMessage().contains("Invalid tag")) {
            throw e;
        }
    }

    @Override
    public void fatalError(SAXParseException e) throws SAXException {
        throw e; // Re-throw fatal errors that can't be recovered from
    }
};

DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setErrorHandler(errorHandler);