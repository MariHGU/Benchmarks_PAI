import java.util.regex.Pattern;
import java.util.regex.Matcher;

public class XMLPreprocessor {
    public static String preprocessXML(String xml) {
        // Regex to match <description>...</description> and replace content with CDATA
        Pattern pattern = Pattern.compile("<description>(.*?)</description>", Pattern.DOTALL);
        Matcher matcher = pattern.matcher(xml);
        String fixedXml = matcher.replaceAll("<description><![CDATA[$1]]></description>");
        return fixedXml;
    }
}