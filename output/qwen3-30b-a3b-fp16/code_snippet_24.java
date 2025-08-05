public class Main {
    public static void main(String[] args) {
        String rawXML = "<xml><description>Example:Description:<THIS-IS-PART-OF-DESCRIPTION></description></xml>";
        
        // Step 1: Preprocess the XML
        String processedXML = XMLPreprocessor.preprocessXML(rawXML);
        
        // Step 2: Parse the processed XML
        try {
            Document doc = XMLParser.parseXML(processedXML);
            // Proceed with DOM manipulation
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}