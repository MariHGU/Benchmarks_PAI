String xmlString = "<xml> ... <description>Example:Description:<THIS-IS-PART-OF-DESCRIPTION></description> ... </xml>";
   
   // Replace content inside description tags with escaped versions of the content
   String cleanedXmlString = xmlString.replaceAll("(?<=<description>).*?(?=</description>)", 
       matcher -> matcher.group().replaceAll("<.*?>", "&lt;$0&gt;"));
   
   DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
   DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
   Document doc = dBuilder.parse(new InputSource(new StringReader(cleanedXmlString)));