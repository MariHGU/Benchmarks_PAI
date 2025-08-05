import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

public class JsoupParser {
    public static void main(String[] args) {
        String invalidXml = "<xml><description>Example:Description:<THIS-IS-PART-OF-DESCRIPTION></description></xml>";
        Document doc = Jsoup.parse(invalidXml, "", Parser.xmlParser());

        // Process the document
        System.out.println(doc.toString());
    }
}