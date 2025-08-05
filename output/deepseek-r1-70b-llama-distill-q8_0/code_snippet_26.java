boolean parsedSuccessfully = false;
while (!parsedSuccessfully) {
    try {
        Document doc = builder.parse(new InputSource(new StringReader(xmlInput)));
        parsedSuccessfully = true;
    } catch (SAXException e) {
        // Attempt to clean the XML and retry
        xmlInput = cleanXml(xmlInput);
    }
}