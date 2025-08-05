import org.cyberneko.html.parsers.SAXParser;

public class RelaxedXmlParser {
    public static Document parseRelaxed(String xml) throws Exception {
        SAXParser parser = new SAXParser();
        InputSource source = new InputSource(new StringReader(xml));
        return parser.parse(source);
    }
}