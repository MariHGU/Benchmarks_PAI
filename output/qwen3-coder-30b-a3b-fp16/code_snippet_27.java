public String escapeDescriptionContent(String xml) {
    // Find description tags and escape their content
    Pattern descPattern = Pattern.compile("<description>(.*?)</description>", 
                                        Pattern.DOTALL);
    return descPattern.matcher(xml).replaceAll(match -> {
        String content = match.group(1);
        // Escape any angle brackets that aren't part of valid XML tags
        String escapedContent = content.replaceAll("(?<!<)<(?!/|\\w)(?![^>]*>)", "&lt;")
                                     .replaceAll("(?<!>)>(?![^>]*>)", "&gt;");
        return "<description>" + escapedContent + "</description>";
    });
}