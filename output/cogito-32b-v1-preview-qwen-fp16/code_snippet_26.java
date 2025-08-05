public class SpecificXmlFixer {
    public static String fixKnownInvalidTags(String xml) {
        // Replace <THIS-IS-PART-OF-DESCRIPTION> with its escaped version only within description tags
        return xml.replaceAll("<description>(.*?)<THIS-IS-PART-OF-DESCRIPTION>", 
                             "<description>$1&lt;THIS-IS-PART-OF-DESCRIPTION&gt;");
    }
}