public class CustomEntityResolver implements EntityResolver {

    private static final String ENTITY_PLACEHOLDER = "##MALFORMED_TAG##";
    private static Pattern MALFORMED_TAG_PATTERN;
    private DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();

    static {
        MALFORMED_TAG_PATTERN = Pattern.compile("<\\/?([a-zA-Z0-9]+):[^>]*>");
    }

    public Document parse(String xml) throws Exception {
        DocumentBuilder db = dbf.newDocumentBuilder();
        db.setEntityResolver(this);
        return db.parse(new InputSource(new StringReader(sanitizeXml(xml))));
    }

    @Override
    public InputSource resolveEntity(String publicId, String systemId) {
        Matcher m = MALFORMED_TAG_PATTERN.matcher(systemId);
        if (m.find()) {
            return new InputSource(new StringReader(ENTITY_PLACEHOLDER));
        } else {
            // For unknown entities, let the default behaviour be applied
            return null;
        }
    }

    private static String sanitizeXml(String xml) {
        Matcher m = MALFORMED_TAG_PATTERN.matcher(xml);
        if (m.find()) {
            throw new IllegalArgumentException("Invalid XML: malformed tag found in leaf element");
        } else {
            return xml;
        }
    }

}