import org.xml.sax.*;
import org.xml.sax.helpers.DefaultHandler;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;
import java.io.StringReader;

public class SAXXMLParser {
    
    public void parseWithSAX(String xmlString) throws Exception {
        SAXParserFactory factory = SAXParserFactory.newInstance();
        SAXParser saxParser = factory.newSAXParser();
        
        MyContentHandler handler = new MyContentHandler();
        saxParser.parse(new InputSource(new StringReader(xmlString)), handler);
    }
    
    class MyContentHandler extends DefaultHandler {
        private StringBuilder currentText = new StringBuilder();
        private boolean inDescription = false;
        
        @Override
        public void startElement(String uri, String localName, String qName, Attributes attributes) {
            if ("description".equalsIgnoreCase(qName)) {
                inDescription = true;
                currentText.setLength(0); // Clear the buffer
            }
        }
        
        @Override
        public void characters(char[] ch, int start, int length) {
            if (inDescription) {
                String text = new String(ch, start, length);
                // Process the text to escape invalid content
                currentText.append(escapeInvalidContent(text));
            }
        }
        
        @Override
        public void endElement(String uri, String localName, String qName) {
            if ("description".equalsIgnoreCase(qName)) {
                inDescription = false;
                String processedContent = currentText.toString();
                // Handle the processed description content here
                System.out.println("Description: " + processedContent);
            }
        }
        
        private String escapeInvalidContent(String text) {
            return text.replaceAll("<", "&lt;")
                      .replaceAll(">", "&gt;");
        }
    }
}