import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

try {
    Document doc = Jsoup.parse(xmlInput);
} catch (Exception e) {
    // Handle parsing errors
}