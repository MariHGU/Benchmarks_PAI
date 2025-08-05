DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
   DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
   Document doc = null;
   
   try {
       doc = dBuilder.parse(new InputSource(new StringReader(xmlString)));
   } catch (SAXParseException e) {
       // Handle the error, for example by cleaning the XML
       String cleanedXmlString = cleanInvalidXml(xmlString);
       doc = dBuilder.parse(new InputSource(new StringReader(cleanedXmlString)));
   }
   
   private static String cleanInvalidXml(String xml) {
       return xml.replaceAll("(?<=<description>).*?(?=</description>)", 
           matcher -> matcher.group().replaceAll("<.*?>", "&lt;$0&gt;"));
   }