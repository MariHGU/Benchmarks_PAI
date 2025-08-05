import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.ByteArrayInputStream;

public class InvalidXmlParserJsoup {

    public static org.jsoup.nodes.Document parseInvalidXml(String xmlString) {
        org.jsoup.nodes.Document document = Jsoup.parse(xmlString);

        // Find the 'description' element
        Element descriptionElement = document.selectFirst("description");

        if (descriptionElement != null) {
            // Remove any child elements that are invalid tags
            for (Element child : descriptionElement.children()) {
                if (!isValidTag(child.tagName())) {
                    child.remove();
                }
            }
        }

        return document;
    }

    private static boolean isValidTag(String tagName) {
        // Add logic to determine if the tag is a valid tag name
        return !tagName.equals("THIS-IS-PART-OF-DESCRIPTION");
    }

    public static void main(String[] args) {
        String invalidXml = "<xml><description>Example:Description:<THIS-IS-PART-OF-DESCRIPTION></description></xml>";
        org.jsoup.nodes.Document document = parseInvalidXml(invalidXml);

        // Process the Jsoup Document...
        System.out.println("XML parsed successfully with Jsoup.");
        System.out.println(document.select("description").text());

    }
}