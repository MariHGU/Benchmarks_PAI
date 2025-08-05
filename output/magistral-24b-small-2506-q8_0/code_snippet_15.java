String cleanedXml = xmlInput.replaceAll(
    "(<description>)(.*?)(</description>)",
    "$1" + escapeTags($2) + "$3"
);
Document doc = DocumentBuilder.parse(cleanedXml);