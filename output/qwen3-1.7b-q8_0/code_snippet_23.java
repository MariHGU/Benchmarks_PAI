public class MyContentHandler implements org.xml.sax.ContentHandler {
    @Override
    public void startDocument() throws SAXException {
        System.out.println("Start of document");
    }

    @Override
    public void endDocument() throws SAXException {
        System.out.println("End of document");
    }

    @Override
    public void startElement(String uri, String localName, String qName, org.xml.sax.Attributes attributes) throws SAXException {
        System.out.println("Start element: " + qName);
    }

    @Override
    public void endElement(String uri, String localName, String qName) throws SAXException {
        System.out.println("End element: " + qName);
    }

    @Override
    public void characters(char[] ch, int start, int length) throws SAXException {
        System.out.println("Characters: " + new String(ch, start, length));
    }

    @Override
    public void error(org.xml.sax.SAXException e) throws SAXException {
        e.printStackTrace();
    }
}