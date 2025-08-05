public Map<String, String> parseDescriptionContent(String xml) {
    Map<String, String> descriptions = new HashMap<>();
    
    Pattern pattern = Pattern.compile("<description>(.*?)</description>", 
                                     Pattern.DOTALL | Pattern.CASE_INSENSITIVE);
    Matcher matcher = pattern.matcher(xml);
    
    while (matcher.find()) {
        String content = matcher.group(1)
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;");
        descriptions.put(matcher.group(0), content);
    }
    
    return descriptions;
}