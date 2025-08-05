import org.jsoup.Jsoup;
import org.w3c.dom.Document;
import javax.xml.parsers.DocumentBuilderFactory;

public class JsoupXmlHandler {
    public static void main(String[] args) throws Exception {
        String input = "<xml>\n" +
                       "  <description>Example:Description:<THIS-IS-PART-OF-DESCRIPTION></description>\n" +
                       "</xml>";

        // Parse the XML with Jsoup
        org.jsoup.nodes.Document jsoupDoc = Jsoup.parse(input, "", org.jsoup.parser.Parser.xmlParser());

        // Convert to w3c Document if needed (optional)
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        factory.setNamespaceAware(true);
        javax.xml.parsers.DocumentBuilder builder = factory.newDocumentBuilder();
        Document doc = builder.parse(new java.io.ByteArrayInputStream(jsoupDoc.html().getBytes()));
    }
}