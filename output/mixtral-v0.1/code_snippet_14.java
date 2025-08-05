import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
...
String dirtyXml = "<xml><description>Example:Description:<THIS-IS-PART-OF-DESCRIPTION></description></xml>"; // Your invalid XML input
Document document = Jsoup.parse(dirtyXml, "", Parser.xmlParser()); // Parse using JSoup with xml parser flag on
String cleanXml = document.toString(); // Your cleaned up XML as a string that can be parsed by regular parsers