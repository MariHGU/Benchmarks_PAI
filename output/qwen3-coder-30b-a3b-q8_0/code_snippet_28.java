public class Main {
    public static void main(String[] args) {
        String malformedXml = "<xml><description>Example:Description:<THIS-IS-PART-OF-DESCRIPTION></description></xml>";
        
        try {
            RobustXMLParser parser = new RobustXMLParser();
            Document doc = parser.parseRobustXML(malformedXml);
            
            // Process your document here
            System.out.println("Successfully parsed XML");
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}