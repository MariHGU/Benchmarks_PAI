import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

public class JsoupXmlParser {
    public static Document parseWithJsoup(String xml) throws Exception {
        return Jsoup.parse(xml, "", Parser.xmlParser());
    }
}