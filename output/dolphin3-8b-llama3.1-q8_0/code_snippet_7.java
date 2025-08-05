try {
    DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
    DocumentBuilder db;
    Document doc;

    // Set up a resolver to handle entity references
    EntityResolver er = new MyEntityResolver();
    
    // Parse the document with error reporting
    db = dbf.newDocumentBuilder();
    db.setErrorStream(System.err);
    
    doc = db.parse(new InputSource(new StringReader(input)), null, er);

} catch (SAXException se) {
   System.out.println("An error occurred during parsing:");
   se.printStackTrace();
   
   // If the exception is caused by malformed XML, try to recover
   if (se.getCause() instanceof javax.xml.parsers.MalformedCoordinateException) {
       // Skip over this element and continue with the next one
       ...
   }
}