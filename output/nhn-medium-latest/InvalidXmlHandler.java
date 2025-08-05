import java.io.StringReader;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import org.xml.sax.ErrorHandler;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;
import org.xml.sax.SAXParseException;

public class InvalidXmlHandler {
    public static Document parseInvalidXml(String xml) throws Exception {
        try (StringReader reader = new StringReader(xml)) {
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();

            // Set custom error handler to ignore errors
            builder.setErrorHandler(new ErrorHandler() {
                @Override
                public void warning(SAXParseException exception) throws SAXException {
                    System.out.println("Warning: " + exception.getMessage());
                }

                @Override
                public void error(SAXParseException exception) throws SAXException {
                    System.out.println("Error: " + exception.getMessage());
                }

                @Override
                public void fatalError(SAXParseException exception) throws SAXException {
                    System.out.println("Fatal Error: " + exception.getMessage());
                }
            });

            return builder.parse(new InputSource(reader));
        }
    }

    public static void main(String[] args) throws Exception {
        String xml = "<xml>" +
                     "  <description>Example:Description:<THIS-IS-PART-OF-DESCRIPTION></description>" +
                     "</xml>";

        Document doc = parseInvalidXml(xml);
        System.out.println("Parsed successfully!");
    }
}