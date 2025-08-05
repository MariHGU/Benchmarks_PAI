public class AdvancedXMLParser {
    
    public Document parseDescriptionTag(String xmlString) throws Exception {
        // First, identify and escape problematic content within description tags
        String processedXml = processDescriptionTags(xmlString);
        
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        return builder.parse(new ByteArrayInputStream(processedXml.getBytes()));
    }
    
    private String processDescriptionTags(String xml) {
        // Find all description tags and their content
        Pattern descPattern = Pattern.compile(
            "<description>(.*?)</description>", 
            Pattern.DOTALL | Pattern.CASE_INSENSITIVE
        );
        
        return descPattern.matcher(xml).replaceAll(matchResult -> {
            String content = matchResult.group(1);
            // Escape any angle brackets that aren't part of valid XML tags
            String escapedContent = escapeInvalidXML(content);
            return "<description>" + escapedContent + "</description>";
        });
    }
    
    private String escapeInvalidXML(String content) {
        // Replace < with &lt; but be careful not to double-escape already escaped content
        return content.replaceAll("<(?![A-Za-z/])", "&lt;")
                    .replaceAll(">", "&gt;");
    }
}