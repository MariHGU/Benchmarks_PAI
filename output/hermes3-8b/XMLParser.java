import org.xml.sax.SAXException;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.ParserConfigurationException;
import org.xml.sax.XMLReader;
import org.xml.sax.helpers.DefaultHandler;

public class XMLParser {
    public void parseXML(String xml) throws ParserConfigurationException, SAXException {
        // Create a DocumentBuilder with custom error handling
        DocumentBuilder builder = DocumentBuilderFactory.newInstance().newDocumentBuilder();
        builder.setEntityResolver(new MyEntityResolver());
        builder.setErrorHandler(new MyErrorHandler());

        // Parse the XML using the lenient DocumentBuilder
        Document document = builder.parse(new InputSource(new StringReader(xml)));

        // Process the parsed document
        // ...

    }

    private class MyEntityResolver extends EntityResolver {
        public InputSource resolveEntity(publicID, systemID) throws SAXException {
            return new InputSource();
        }
    }

    private class MyErrorHandler implements ErrorHandler {
        public void warning(SAXParseException exception) throws SAXException {}
        public void error(SAXParseException exception) throws SAXException {}
        public void fatalError(SAXParseException exception) throws SAXException {}
    }
}