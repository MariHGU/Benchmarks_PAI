String xml = "<xml> ... <description>Example:Description:<THIS-IS-PART-OF-DESCRIPTION></description> ... </xml>";
String processedXml = xml.replace("<description>", "<description>").replace("</description>", "</description>");

// Replace any occurrences of '<' and '>' within the <description> tag with their XML entities
processedXml = processedXml.replaceAll("(<description>.*?)(<.*?>)(</description>)", "$1&lt;$2&gt;$3");

DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
DocumentBuilder builder = factory.newDocumentBuilder();
Document document = builder.parse(new InputSource(new StringReader(processedXml)));