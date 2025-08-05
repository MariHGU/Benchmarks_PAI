import org.xml.sax.*;
import org.xml.sax.helpers.DefaultHandler;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;

public class LenientXMLReader {
    
    public Document parseLeniently(String xmlString) throws Exception {
        // First try normal parsing
        try {
            return parseNormally(xmlString);
        } catch (Exception e) {
            // If that fails, try to fix it
            String fixedXml = repairInvalidXML(xmlString);
            return parseNormally(fixedXml);
        }
    }
    
    private String repairInvalidXML(String xml) {
        // Simple fix: wrap problematic content in CDATA
        return xml.replaceAll(
            "<description>([^<]*(?:<(?!/description>)[^<]*)*?)</description>",
            "<description><![CDATA[$1]]></description>"
        );
    }
    
    private Document parseNormally(String xml) throws Exception {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        return builder.parse(new ByteArrayInputStream(xml.getBytes()));
    }
}