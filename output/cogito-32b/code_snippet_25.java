XMLInputFactory factory = XMLInputFactory.newInstance();
XMLEventReader eventReader = factory.createXMLEventReader(new StringReader(xml));

while(eventReader.hasNext()) {
    XMLEvent event = eventReader.nextEvent();
    if(event.isStartElement() && "description".equals(event.asStartElement().getName().getLocalPart())) {
        // Handle description content here
        while(!(event = eventReader.nextEvent()).isEndElement());
    }
}