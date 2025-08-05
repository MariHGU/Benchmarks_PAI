public String fixDescriptionTags(String xml) {
    // This pattern looks for description tags and escapes their content
    return xml.replaceAll(
        "<description>(.*?)</description>", 
        "<description>$1</description>"
    ).replaceAll("<([^/>]+)>", "&lt;$1&gt;");
}