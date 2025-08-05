import org.jtidy.Tidy;
import org.xml.sax.InputSource;

Tidy tidy = new Tidy();
tidy.setShowWarnings(false);
tidy.setQuiet(true);

InputStream in = // your input stream
Document doc = tidy.parseDOM(in, null);