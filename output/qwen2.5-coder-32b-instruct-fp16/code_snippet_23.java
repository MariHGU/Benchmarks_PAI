// Using TagSoup to parse the HTML-like XML
   SAXParserFactory factory = SAXParserFactory.newInstance();
   SAXParser saxParser = factory.newSAXParser();

   Parser parser = new Parser();  // TagSoup parser
   parser.setFeature(Parser.namespacesFeature, false);
   parser.setContentHandler(new DefaultHandler() {
       @Override
       public void characters(char[] ch, int start, int length) throws SAXException {
           System.out.println("Characters: " + new String(ch, start, length));
       }
   });

   InputSource is = new InputSource(new StringReader(xmlString));
   parser.parse(is);