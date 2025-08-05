import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import java.io.ByteArrayInputStream;
import java.io.IOException;

public class InvalidXmlParser {

    public static Document parseInvalidXml(String xmlString) throws Exception {
        // Replace the invalid tag before parsing
        String cleanedXml = xmlString.replace("<THIS-IS-PART-OF-DESCRIPTION>", "");
        cleanedXml = cleanedXml.replace("</THIS-IS-PART-OF-DESCRIPTION>", "");

        ByteArrayInputStream inputStream = new ByteArrayInputStream(cleanedXml.getBytes());

        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        Document document = builder.parse(inputStream);
        inputStream.close();  // important to close the stream
        return document;
    }

    public static void main(String[] args) {
        String invalidXml = "<xml><description>Example:Description:<THIS-IS-PART-OF-DESCRIPTION></description></xml>";

        try {
            Document document = parseInvalidXml(invalidXml);
            // Process the document...
            System.out.println("XML parsed successfully.");
        } catch (Exception e) {
            System.err.println("Error parsing XML: " + e.getMessage());
            e.printStackTrace();
        }
    }
}