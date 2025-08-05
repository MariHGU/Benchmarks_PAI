// Replace < and > with &lt; and &gt;
String modifiedXML = xml.replaceAll("<", "&lt;")
                       .replaceAll(">", "&gt;");
DocumentBuilder builder = DocumentBuilderFactory.newInstance().newDocumentBuilder();
Document doc = builder.parse(new InputSource(new StringReader(modifiedXML)));