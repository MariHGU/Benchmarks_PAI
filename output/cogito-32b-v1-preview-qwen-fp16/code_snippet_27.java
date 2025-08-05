import javax.xml.parsers.*;
import org.xml.sax.*;

public class LenientXmlParser {
    public static Document parseWithErrorHandler(String xml) throws Exception {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        factory.setValidating(false);
        
        DocumentBuilder builder = factory.newDocumentBuilder();
        builder.setErrorHandler(new ErrorHandler() {
            @Override
            public void warning(SAXParseException exception) throws SAXException {}
            
            @Override
            public void error(SAXParseException exception) throws SAXException {}
            
            @Override
            public void fatalError(SAXParseException exception) throws SAXException {}
        });
        
        return builder.parse(new InputSource(new StringReader(xml)));
    }
}