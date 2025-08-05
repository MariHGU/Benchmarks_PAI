import javax.xml.stream.*;

public class StaxXmlParser {
    public static void parseWithStax(String xml) throws Exception {
        XMLInputFactory factory = XMLInputFactory.newInstance();
        InputStream stream = new ByteArrayInputStream(xml.getBytes());
        XMLStreamReader reader = factory.createXMLStreamReader(stream);
        
        while(reader.hasNext()) {
            int event = reader.next();
            switch(event) {
                case XMLStreamConstants.START_ELEMENT:
                    String elementName = reader.getLocalName();
                    // Process element
                    break;
                case XMLStreamConstants.CHARACTERS:
                    String text = reader.getText().trim();
                    if (!text.isEmpty()) {
                        // Handle text content, possibly escaping problematic parts
                    }
                    break;
            }
        }
    }
}