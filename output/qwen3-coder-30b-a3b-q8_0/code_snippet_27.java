public class RobustXMLParser {
    
    public Document parseRobustXML(String xmlString) throws Exception {
        // Handle the specific case in your example
        String cleanedXml = cleanDescriptionTags(xmlString);
        
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        return builder.parse(new ByteArrayInputStream(cleanedXml.getBytes()));
    }
    
    private String cleanDescriptionTags(String xml) {
        // More precise pattern matching for your specific case
        Pattern pattern = Pattern.compile(
            "<description>([^<]*(?:<(?!/description>)[^<]*)*)</description>", 
            Pattern.DOTALL
        );
        
        return pattern.matcher(xml).replaceAll(matchResult -> {
            String content = matchResult.group(1);
            // Escape any remaining angle brackets in the content
            String escapedContent = escapeAngleBrackets(content);
            return "<description>" + escapedContent + "</description>";
        });
    }
    
    private String escapeAngleBrackets(String content) {
        // Replace < with &lt; and > with &gt;
        return content.replace("<", "&lt;")
                     .replace(">", "&gt;");
    }
}