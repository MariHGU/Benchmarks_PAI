MyContentHandler handler = new MyContentHandler();
   MyErrorHandler errorhandler = new MyErrorHandler();

   reader.setContentHandler(handler);
   reader.setErrorHandler(errorhandler);

   try {
       reader.parse(xmlString);
   } catch (SAXException e) {
       errorhandler.fatalError(e);
   }