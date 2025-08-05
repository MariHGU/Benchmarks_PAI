import java.io.StringReader;
import java.io.StringWriter;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import org.xml.sax.InputSource;

public class InvalidXmlHandler1 {
    public static Document parseInvalidXml(String xml) throws Exception {
        // Remove invalid tags in the description element
        String cleanedXml = xml.replaceAll("<description>[^<]*<(.*?)>([^>]*)</description>",
                                           "<description>$2</description>");

        try (StringReader reader = new StringReader(cleanedXml)) {
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
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