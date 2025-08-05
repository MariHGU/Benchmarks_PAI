import javax.xml.parsers.DocumentBuilder;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;

public class XMLParser {
    public static void main(String[] args) throws Exception {
        String invalidXml = "<xml><description>Example:Description:<THIS-IS-PART-OF-DESCRIPTION></description></xml>";
        
        DocumentBuilder db = DocumentBuilderFactory.newInstance().newDocumentBuilder();
        Document doc = db.parse(new java.io.ByteArrayInputStream(invalidXml.getBytes()));
        
        NodeList descriptionNodes = doc.getElementsByTagName("description");
        for (int i = 0; i < descriptionNodes.getLength(); i++) {
            String text = descriptionNodes.item(i).getTextContent();
            // Remove any nested tags
            String cleanedText = text.replaceAll("<[^>]+>", "");
            System.out.println(cleanedText);
        }
    }
}