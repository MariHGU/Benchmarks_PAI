import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class XmlSanitizer {

    public static void main(String[] args) {
        try {
            // Sample XML input
            String invalidXml = "<xml>" +
                    "  <description>Example:Description:<THIS-IS-PART-OF-DESCRIPTION></description>" +
                    "</xml>";

            // Sanitize the XML content
            String sanitizedXml = sanitizeXml(invalidXml);

            // Parse the sanitized XML using DocumentBuilder
            Document document = parseXml(sanitizedXml);

            // Process the document as needed...
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static String sanitizeXml(String xml) {
        // Regular expression to find invalid tags inside <description> elements
        Pattern pattern = Pattern.compile("<description>(.*?)</description>", Pattern.DOTALL);
        Matcher matcher = pattern.matcher(xml);

        StringBuffer sanitizedXml = new StringBuffer();
        while (matcher.find()) {
            // Replace any angle brackets with their HTML entities within description tags
            String descriptionContent = matcher.group(1)
                    .replaceAll("<", "&lt;")
                    .replaceAll(">", "&gt;");
            matcher.appendReplacement(sanitizedXml, "<description>" + descriptionContent + "</description>");
        }
        matcher.appendTail(sanitizedXml);

        return sanitizedXml.toString();
    }

    public static Document parseXml(String xml) throws Exception {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();

        InputStream inputStream = new ByteArrayInputStream(xml.getBytes(StandardCharsets.UTF_8));
        return builder.parse(inputStream);
    }
}