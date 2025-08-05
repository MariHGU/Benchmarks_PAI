import org.htmlcleaner.*;

HTMLCleaner cleaner = new HTMLCleaner();
TagNode node = cleaner.clean(invalidXml);
// Convert to DOM if needed
Document doc = new DomSerializer(new CleanerProperties()).createDOM(node);