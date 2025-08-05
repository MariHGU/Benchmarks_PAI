String cleanXml(String xml) {
    // Find all <description> elements and their content
    Pattern pattern = Pattern.compile("<description>(.*?)</description>");
    Matcher matcher = pattern.matcher(xml);
    
    StringBuffer result = new StringBuffer();
    while (matcher.find()) {
        String descriptionContent = matcher.group(1);
        // Escape any nested tags within the description
        String cleanDescription = descriptionContent.replaceAll("<", "&lt;")
                                                   .replaceAll(">", "&gt;");
        matcher.appendReplacement(result, "<description>" + cleanDescription + "</description>");
    }
    matcher.appendTail(result);
    
    return result.toString();
}

// Usage:
String invalidXml = "... <description>Example:Description:<THIS-IS-PART-OF-DESCRIPTION></description> ...";
String cleanedXml = cleanXml(invalidXml);
Document doc = DocumentBuilder.parse(new InputSource(new StringReader(cleanedXml)));