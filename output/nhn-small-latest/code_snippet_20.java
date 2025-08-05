TransformerFactory transformerFactory = TransformerFactory.newInstance();
Transformer transformer = transformerFactory.newTransformer(new StreamSource("remove-tags.xslt"));
StringReader reader = new StringReader(xmlString);
StringWriter writer = new StringWriter();
transformer.transform(new StreamSource(reader), new StreamResult(writer));
String cleanedXml = writer.toString();

DocumentBuilder builder = DocumentBuilderFactory.newInstance().newDocumentBuilder();
Document doc = builder.parse(new InputSource(new StringReader(cleanedXml)));