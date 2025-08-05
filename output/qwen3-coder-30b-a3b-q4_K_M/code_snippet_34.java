// Using JDOM (add dependency)
import org.jdom2.Document;
import org.jdom2.input.SAXBuilder;

SAXBuilder builder = new SAXBuilder();
Document doc = builder.build(new StringReader(xmlString));