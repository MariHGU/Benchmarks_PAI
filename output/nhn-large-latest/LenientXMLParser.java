import com.fasterxml.aalto_xml.io.XMLStreamReader;
import java.io.StringReader;

public class LenientXMLParser {
    public static void main(String[] args) throws Exception {
        String invalidXml = "<xml><description>Example:Description:<THIS-IS-PART-OF-DESCRIPTION></description></xml>";
        
        XMLStreamReader reader = XMLStreamReader.newInstance();
        reader.setLenient(true);
        reader.setInput(new StringReader(invalidXml));
        
        while (reader.next() != XMLStreamConstants.END_DOCUMENT) {
            if (reader.getEventType() == XMLStreamConstants.START_ELEMENT) {
                System.out.println("Element: " + reader.getLocalName());
            } else if (reader.getEventType() == XMLStreamConstants.CHARACTERS) {
                String text = reader.getText().replaceAll("<[^>]+>", "");
                System.out.println("Text: " + text);
            }
        }
    }
}