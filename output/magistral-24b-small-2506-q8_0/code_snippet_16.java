String cleanedXml = originalXml.replaceAll(
    "<description>(.*?)</description>",
    match -> {
        String content = match.group(1);
        String escapedContent = content.replaceAll("<([^>]+)>", "&lt;$1&gt;");
        return "<description>" + escapedContent + "</description>";
    }
);