import javax.xml.parsers.DocumentBuilder;
import org.w3c.dom.Document;

public class SafeXMLParser {
    public static void main(String[] args) {
        String invalidXml = "<xml><description>Example:Description:<THIS-IS-PART-OF-DESCRIPTION></description></xml>";
        
        try {
            DocumentBuilder db = DocumentBuilderFactory.newInstance().newDocumentBuilder();
            Document doc = db.parse(new java.io.ByteArrayInputStream(invalidXml.getBytes()));
            
            // Process document
            System.out.println("Parsing succeeded!");
        } catch (Exception e) {
            System.err.println("Error parsing XML: " + e.getMessage());
            // Implement recovery logic here, e.g., log and continue
        }
    }
}