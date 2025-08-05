DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
     factory.setValidating(false);
     factory.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false);