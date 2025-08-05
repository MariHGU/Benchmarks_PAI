import java.util.regex.Pattern;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;

public class InvalidXmlHandler {
    public static void main(String[] args) throws Exception {
        String input = "<xml>\n" +
                       "  <description>Example:Description:<THIS-IS-PART-OF-DESCRIPTION></description>\n" +
                       "</xml>";

        // Preprocess the XML to escape invalid tags
        Pattern pattern = Pattern.compile("<(?!\\/?[a-zA-Z]:|\\/?\\w+:)\\/?[^>]+>");
        String processedInput = pattern.matcher(input).replaceAll(match -> {
            return match.group().replace("<", "&lt;").replace(">", "&gt;");
        });

        // Parse the preprocessed XML
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        Document doc = builder.parse(new java.io.ByteArrayInputStream(processedInput.getBytes()));
    }
}