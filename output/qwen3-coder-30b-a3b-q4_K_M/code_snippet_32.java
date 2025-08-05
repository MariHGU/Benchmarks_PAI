import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import java.io.ByteArrayInputStream;

public Document parseInvalidXml(String xmlString) throws Exception {
    // Escape invalid XML characters in text content
    String escapedXml = escapeInvalidXmlCharacters(xmlString);
    
    DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
    DocumentBuilder builder = factory.newDocumentBuilder();
    return builder.parse(new ByteArrayInputStream(escapedXml.getBytes("UTF-8")));
}

private String escapeInvalidXmlCharacters(String xml) {
    // This approach assumes you know the structure and can target specific elements
    // For your case, you want to escape content within description tags
    
    StringBuilder result = new StringBuilder();
    int i = 0;
    
    while (i < xml.length()) {
        if (xml.substring(i).startsWith("<description>")) {
            int descStart = i;
            int descEnd = xml.indexOf("</description>", descStart);
            
            if (descEnd != -1) {
                // Extract the description content
                String descriptionContent = xml.substring(descStart + 13, descEnd);
                
                // Escape problematic characters
                String escapedContent = descriptionContent
                    .replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;");
                
                // Rebuild the XML with escaped content
                result.append(xml.substring(i, descStart + 13))
                      .append(escapedContent)
                      .append(xml.substring(descEnd));
                
                i = descEnd + 12; // Move past </description>
                continue;
            }
        }
        result.append(xml.charAt(i));
        i++;
    }
    
    return result.toString();
}