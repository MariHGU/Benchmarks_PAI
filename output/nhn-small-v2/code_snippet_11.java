SAXParser parser = SAXParserFactory.newInstance().newSAXParser();
CustomXMLFilter filter = new CustomXMLFilter();
parser.parse(inputSource, filter);