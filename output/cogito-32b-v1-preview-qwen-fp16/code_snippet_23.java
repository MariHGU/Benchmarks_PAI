public static String sanitizeXml(String xml) {
    return xml.replaceAll("<[^>]+>", "&lt;$0&gt;"); // Replaces < and > with &lt; and &gt;
}