public class MyContentHandler implements ContentHandler {
       private final List<String> elements = new ArrayList<>();

       @Override
       public void startElement(String namespaceURI, String localName, String qName, Attributes attributes) {
           elements.add(localName);
       }

       @Override
       public void endElement(String namespaceURI, String localName, String qName) {
           if (localName.equals("description")) {
               // Process the element
               System.out.println("Description element found: " + localName);
           }
       }

       @Override
       public void startDocument() {
           // Called when the document starts
       }

       @Override
       public void endDocument() {
           // Called when the document ends
       }

       @Override
       public void characters(char[] ch, int start, int length) {
           // Process character data
           String text = new String(ch, start, length);
           System.out.println("Text: " + text);
       }

       public List<String> getElements() {
           return elements;
       }
   }