public String cleanXML(String dirtyXml) {
    // Replace any angle brackets inside description tag with HTML entities
    Pattern pattern = Pattern.compile("<description>(.*?)</description>", 
                                     Pattern.DOTALL | Pattern.CASE_INSENSITIVE);
    Matcher matcher = pattern.matcher(dirtyXml);
    
    StringBuffer cleanedXml = new StringBuffer();
    while (matcher.find()) {
        String content = matcher.group(1)
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;");
        matcher.appendReplacement(cleanedXml, 
            "<description>" + content + "</description>");
    }
    matcher.appendTail(cleanedXml);
    
    return cleanedXml.toString();
}