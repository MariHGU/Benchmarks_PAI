import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import java.io.ByteArrayInputStream;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class InvalidXmlParserRegex {

    public static Document parseInvalidXml(String xmlString) throws Exception {
        // Regular expression to match the invalid tag
        Pattern pattern = Pattern.compile("<THIS-IS-PART-OF-DESCRIPTION>.*?</THIS-IS-PART-OF-DESCRIPTION>", Pattern.DOTALL);
        Matcher matcher = pattern.matcher(xmlString);

        String cleanedXml = matcher.replaceAll("");

        ByteArrayInputStream inputStream = new ByteArrayInputStream(cleanedXml.getBytes());

        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        Document document = builder.parse(inputStream);
        inputStream.close();
        return document;
    }
    // ... rest of the code (main method) similar to the previous example
}