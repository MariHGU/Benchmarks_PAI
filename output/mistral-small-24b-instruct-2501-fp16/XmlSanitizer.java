import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class XmlSanitizer {
    public static String sanitizeXml(String xml) {
        // Pattern to match invalid tags within description elements
        Pattern pattern = Pattern.compile("<description>(.*?)</description>", Pattern.DOTALL);
        Matcher matcher = pattern.matcher(xml);

        StringBuffer sb = new StringBuffer();
        while (matcher.find()) {
            String descriptionContent = matcher.group(1);
            // Escape any invalid tags within the description content
            descriptionContent = descriptionContent.replaceAll("<[^>]*>", "");
            matcher.appendReplacement(sb, "<description>" + descriptionContent + "</description>");
        }
        matcher.appendTail(sb);

        return sb.toString();
    }

    public static void main(String[] args) {
        String invalidXml = "<xml><description>Example:Description:<THIS-IS-PART-OF-DESCRIPTION></description></xml>";
        String sanitizedXml = sanitizeXml(invalidXml);
        System.out.println(sanitizedXml);

        // Now you can parse the sanitized XML
        try {
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            Document doc = builder.parse(new ByteArrayInputStream(sanitizedXml.getBytes()));
            // Process the document
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}