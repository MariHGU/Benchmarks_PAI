public class MyErrorHandler implements ErrorHandler {
       @Override
       public void error(SAXParseException e) {
           System.err.println("Error: " + e.getMessage());
           e.printStackTrace();
       }

       @Override
       public void fatalError(SAXParseException e) {
           System.err.println("Fatal Error: " + e.getMessage());
           e.printStackTrace();
       }

       @Override
       public void warning(SAXParseException e) {
           System.err.println("Warning: " + e.getMessage());
           e.printStackTrace();
       }
   }