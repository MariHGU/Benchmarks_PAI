import org.jsoup.Jsoup;
import org.w3c.dom.Document;
import javax.xml.parsers.DocumentBuilderFactory;

public class InvalidXmlHandler2 {
    public static Document parseInvalidXml(String xml) throws Exception {
        // Parse using JSoup, which is more tolerant of malformed XML
        String cleanedXml = Jsoup.parse(xml).html();

        try (StringReader reader = new StringReader(cleanedXml)) {
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            return factory.newDocumentBuilder().parse(new InputSource(reader));
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