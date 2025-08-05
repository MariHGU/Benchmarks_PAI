import javax.xml.stream.XMLInputFactory;
import javax.xml.stream.XMLStreamConstants;
import javax.xml.stream.XMLStreamReader;

// Create an input factory
XMLInputFactory factory = XMLInputFactory.newInstance();
factory.setValidating(false);

// Create a new stream reader
try (XMLStreamReader reader = factory.createXMLStreamReader(new StringReader(xmlInput))) {
    while (reader.hasNext()) {
        int eventType = reader.next();
        switch (eventType) {
            case XMLStreamConstants.START_ELEMENT:
                // Handle start element
                break;
            case XMLStreamConstants.CHARACTERS:
                // Handle character data
                break;
            case XMLStreamConstants.END_ELEMENT:
                // Handle end element
                break;
            default:
                // Handle other event types
        }
    }
} catch (Exception e) {
    // Handle parsing errors
}