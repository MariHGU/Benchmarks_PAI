public class XMLCleaner {
    public static void main(String[] args) {
        String invalidXml = "<xml><description>Example:Description:<THIS-IS-PART-OF-DESCRIPTION></description></xml>";
        
        // Clean nested tags within description
        String cleanedXml = invalidXml.replaceAll(
            "(?<=<description>)(.*?)(?=<\\/description>)",
            "$1".replaceAll("<[^>]+>", "") // Remove all HTML tags
        );
        
        System.out.println(cleanedXml);
    }
}