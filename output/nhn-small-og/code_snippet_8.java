import javax.xml.stream.*;
import java.io.StringReader;

public class Main {
    public static void main(String[] args) throws XMLStreamException, IOException {
        String xml = "<xml>\n" +
                " ... \n" +
                "<description>Example:Description:<THIS-IS-PART-OF-DESCRIPTION></description>\n" +
                " ... \n" +
                "</xml>";

        XMLInputFactory factory = XMLInputFactory.newInstance();
        XMLEventReader reader = factory.createXMLEventReader(new StringReader(xml));

        // Create an event loop to process the XML events
        while (reader.hasNext()) {
            XMLEvent event = reader.nextEvent();
            if (event.isStartElement()) {
                StartElement startElement = event.asStartElement();
                String elementName = startElement.getName().getLocalPart();

                // Check for the description tag and handle any unexpected content inside it
                if ("description".equals(elementName)) {
                    StringBuilder buffer = new StringBuilder();
                    boolean inDescription = true;
                    while (reader.hasNext() && inDescription) {
                        XMLEvent nextEvent = reader.nextEvent();
                        if (nextEvent.isStartElement()) {
                            StartElement nextStartElement = nextEvent.asStartElement();
                            String nextElementName = nextStartElement.getName().getLocalPart();
                            if (!"THIS-IS-PART-OF-DESCRIPTION".equals(nextElementName)) {
                                inDescription = false;
                            }
                        } else if (nextEvent.isEndElement()) {
                            EndElement nextEndElement = nextEvent.asEndElement();
                            if ("description".equals(nextEndElement.getName().getLocalPart())) {
                                // Handle the description content here
                                String descriptionContent = buffer.toString();
                                // Process the description as needed
                            }
                        } else {
                            buffer.append(nextEvent.asCharacters().getData());
                        }
                    }
                }
            }
        }
    }
}