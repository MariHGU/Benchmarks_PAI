// Using Jackson XML
ObjectMapper xmlMapper = new XmlMapper();
xmlMapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
YourClass obj = xmlMapper.readValue(invalidXml, YourClass.class);

// Or using Simple XML
Serializer serializer = new Persister(new AnnotationStrategy());
YourClass obj = serializer.read(YourClass.class, invalidXml);