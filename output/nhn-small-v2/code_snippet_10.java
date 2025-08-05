import javax.xml.parsers.SAXParserFactory;
import javax.xml.parsers.XMLFilter;
import javax.xml.parsers.SAXParser;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.sax.SAXTransformerFactory;
import javax.xml.transform.sax.TransformerHandler;
import org.xml.sax.*;
import org.xml.sax.helpers.DefaultHandler;

public class CustomXMLFilter extends XMLFilterImpl {
    private String[] invalidTags = {"THIS-IS-PART-OF-DESCRIPTION"};
    private EntityResolver entityResolver = new EntityResolver() {
        @Override
        public InputSource resolveEntity(String publicId, String systemId) throws SAXException, IOException {
            if (publicId != null && publicId.equals("-//W3C//DTD XML Entity Example//EN")) {
                return new InputSource(new StringReader("<" + invalidTags[0] + "/>"));
            }
            return null;
        }
    };

    public CustomXMLFilter() throws SAXException {
        super(new DefaultHandler());
        SAXParserFactory factory = SAXParserFactory.newInstance();
        factory.setNamespaceAware(true);
        SAXTransformerFactory transformerFactory = (SAXTransformerFactory) TransformerFactory.newInstance();
        TransformerHandler handler = transformerFactory.newTransformer();
        this.setContentHandler(this.getParent() != null ? this.getParent().getContentHandler() : this);
        this.setDTDHandler(new DTDHandler() {
            @Override
            public void setDocumentLocator(Locator locator) {}
            @Override
            public void parseDTD(InputSource inputSource) throws SAXException {
                inputSource.getSystemId(); // Ignore DTD to avoid issues with invalid entities
            }
            @Override
            public void notification(String name, Attributes attributes) throws SAXException {}
        });
        this.setErrorHandler(new ErrorHandler() {
            @Override
            public void warning(SAXParseException exception) throws SAXException {
                System.err.println("Warning: " + exception);
            }
            @Override
            public void error(SAXParseException exception) throws SAXException {
                throw exception;
            }
            @Override
            public void fatalError(SAXParseException exception) throws SAXException {
                throw exception;
            }
        });
        this.setEntityResolver(entityResolver);
    }

    @Override
    public void startElement(String uri, String localName, String qName, Attributes attributes) throws SAXException {
        // Check for invalid tags
        if (Arrays.asList(invalidTags).contains(qName)) {
            System.out.println("Invalid tag encountered: " + qName);
        } else {
            super.startElement(uri, localName, qName, attributes);
        }
    }
}