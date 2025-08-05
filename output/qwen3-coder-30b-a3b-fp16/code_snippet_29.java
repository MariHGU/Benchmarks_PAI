// With JDOM2
import org.jdom2.input.SAXBuilder;
import org.jdom2.Document;

public Document parseWithJDOM(String xmlString) throws Exception {
    SAXBuilder builder = new SAXBuilder();
    // JDOM2 is somewhat more tolerant of malformed XML
    return builder.build(new StringReader(xmlString));
}