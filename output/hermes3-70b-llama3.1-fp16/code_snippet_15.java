import java.util.regex.Pattern;

String xmlString = "...<description>Example:Description:<THIS-IS-PART-OF-DESCRIPTION></description>...";

// Regular expression pattern to match invalid tags within the description element
Pattern pattern = Pattern.compile("<description>(.*?)</description>", Pattern.DOTALL);

// Replace the matched description content with cleaned-up version
xmlString = pattern.matcher(xmlString).replaceAll("<description>$1</description>");

// Now you can parse the modified XML string using DocumentBuilder
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
DocumentBuilder builder = factory.newDocumentBuilder();
Document document = builder.parse(new InputSource(new StringReader(xmlString)));