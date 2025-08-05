// Define a more permissive schema that allows such content
RelaxNGParser parser = new RelaxNGParser();
Schema schema = parser.parse(yourSchemaFile);
DocumentBuilder builder = DocumentBuilderFactory.newInstance().newDocumentBuilder();
builder.setValidating(true);
builder.setSchema(schema);

Document doc = builder.parse(xmlInputStream);