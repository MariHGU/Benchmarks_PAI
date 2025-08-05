import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import java.io.ByteArrayInputStream;
import java.util.regex.Pattern;

public class MalformedXMLParser {
    
    public Document parseMalformedXML(String xmlString) throws Exception {
        // Replace the problematic nested tags with escaped content
        String cleanedXml = escapeInvalidTags(xmlString);
        
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        return builder.parse(new ByteArrayInputStream(cleanedXml.getBytes()));
    }
    
    private String escapeInvalidTags(String xml) {
        // Pattern to match tags that are not properly closed
        // This looks for <word> patterns that aren't part of valid XML structure
        Pattern pattern = Pattern.compile("<([A-Z0-9_-]+)>", Pattern.MULTILINE);
        
        // Simple approach: escape the problematic content
        return xml.replaceAll("<([A-Z0-9_-]+)>", "&lt;$1&gt;");
    }
}