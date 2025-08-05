String xml = "...";
// Replace the invalid content with something that preserves its meaning
xml = xml.replaceAll("<([^>]+)>", "&lt;$1&gt;");
Document doc = DocumentBuilder.parse(xml);