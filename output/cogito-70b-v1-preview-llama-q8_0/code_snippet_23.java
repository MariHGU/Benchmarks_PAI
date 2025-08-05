public Document parseMalformedXML(String xml) throws IOException {
    // Parse using JSoup's XML parser
    Document doc = Jsoup.parse(xml, "", Parser.xmlParser());
    return doc;
}