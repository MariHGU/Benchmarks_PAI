import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import java.io.ByteArrayInputStream;
import java.util.regex.Pattern;

public class FaultTolerantXMLParser {
    
    public Document parseWithFaultTolerance(String xmlString) throws Exception {
        // Escape the problematic content
        String processedXml = escapeInvalidTags(xmlString);
        
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        return builder.parse(new ByteArrayInputStream(processedXml.getBytes("UTF-8")));
    }
    
    private String escapeInvalidTags(String xml) {
        // Pattern to match content between < and > that doesn't contain valid XML tag structure
        // This catches the problematic case: <THIS-IS-PART-OF-DESCRIPTION>
        return xml.replaceAll("(?<=<[^>]*>)((?!<[a-zA-Z][^>]*>)[^<]*)(?=<[^>]*>)", 
                             "<![CDATA[$1]]>");
    }
}