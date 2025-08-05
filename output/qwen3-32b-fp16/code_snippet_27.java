import java.util.regex.*;
import javax.xml.parsers.*;
import org.w3c.dom.*;
import java.io.*;

public class XMLParser {
    public static void main(String[] args) throws Exception {
        // Example XML with invalid content in <description>
        String xml = "<xml><description>Example:Description:<THIS-IS-PART-OF-DESCRIPTION></description></xml>";

        // Preprocess the XML to escape invalid characters in <description>
        String fixedXml = preprocessDescription(xml);

        // Parse the fixed XML using DocumentBuilder
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        InputSource is = new InputSource(new StringReader(fixedXml));
        Document doc = builder.parse(is);

        // Output the parsed description content
        NodeList descriptions = doc.getElementsByTagName("description");
        for (int i = 0; i < descriptions.getLength(); i++) {
            System.out.println("Description: " + descriptions.item(i).getTextContent());
        }
    }

    private static String preprocessDescription(String xml) {
        // Use a regex to find all <description>...</description> blocks
        Pattern pattern = Pattern.compile("<description>(.*?)</description>", Pattern.DOTALL);
        Matcher matcher = pattern.matcher(xml);
        StringBuffer sb = new StringBuffer();

        while (matcher.find()) {
            String content = matcher.group(1);
            // Escape < and > in the description content
            String escapedContent = content.replace("<", "&lt;").replace(">", "&gt;");
            // Replace the original content with escaped version
            matcher.appendReplacement(sb, "<description>" + escapedContent + "</description>");
        }
        matcher.appendTail(sb);
        return sb.toString();
    }
}