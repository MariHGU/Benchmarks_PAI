public class CustomXMLParser {
    public String stripInternalTags(String xml) {
        return xml.replaceAll("<THIS-IS-PART-OF-DESCRIPTION>.*?</THIS-IS-PART-OF-DESCRIPTION>", "");
    }
    
    public Document parse(String cleanedXml) throws ParserConfigurationException, SAXException, IOException {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        return builder.parse(new InputSource(new StringReader(cleanedXml)));
    }
}