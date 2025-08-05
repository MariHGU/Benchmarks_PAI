import java.util.regex.Pattern;

public class XmlPreprocessor {
    public static String preprocessXml(String xml) {
        // Regular expression pattern to match invalid tags within leaf tags
        String regex = "<[^>]+>";
        
        // Replace invalid tags with empty strings
        return Pattern.compile(regex).matcher(xml).replaceAll("");
    }
}