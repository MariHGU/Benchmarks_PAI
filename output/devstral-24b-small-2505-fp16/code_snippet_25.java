import org.xml.sax.*;
import org.xml.sax.helpers.DefaultHandler;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;

public class LenientXmlHandler extends DefaultHandler {
    private StringBuilder currentValue = new StringBuilder();
    private boolean inDescription = false;

    public static void main(String[] args) throws Exception {
        String input = "<xml>\n" +
                       "  <description>Example:Description:<THIS-IS-PART-OF-DESCRIPTION></description>\n" +
                       "</xml>";

        SAXParserFactory factory = SAXParserFactory.newInstance();
        factory.setValidating(false);
        SAXParser saxParser = factory.newSAXParser();

        LenientXmlHandler handler = new LenientXmlHandler();
        saxParser.parse(new java.io.ByteArrayInputStream(input.getBytes()), handler);

        System.out.println("Parsed description: " + handler.currentValue.toString());
    }

    @Override
    public void startElement(String uri, String localName, String qName, Attributes attributes) throws SAXException {
        if ("description".equals(qName)) {
            inDescription = true;
        }
        // Ignore other elements
    }

    @Override
    public void endElement(String uri, String localName, String qName) throws SAXException {
        if ("description".equals(qName)) {
            inDescription = false;
        }
    }

    @Override
    public void characters(char[] ch, int start, int length) throws SAXException {
        if (inDescription) {
            currentValue.append(ch, start, length);
        }
    }
}