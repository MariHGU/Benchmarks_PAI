public class XMLParser {
    public static void main(String[] args) {
        try {
            SAXParserFactory factory = SAXParserFactory.newInstance();
            SAXParser parser = factory.newSAXParser();
            XMLReader xmlReader = parser.getXMLReader();

            MyContentHandler handler = new MyContentHandler();
            xmlReader.setContentHandler(handler);

            File file = new File("invalid.xml");
            InputSource is = new InputSource(file.toURI().toURL().openStream());

            xmlReader.parse(is);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}