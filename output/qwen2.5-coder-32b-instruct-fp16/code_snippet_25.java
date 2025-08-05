Pattern pattern = Pattern.compile("<description>(.*?)</description>");
   Matcher matcher = pattern.matcher(xmlString);
   
   while (matcher.find()) {
       String descriptionContent = matcher.group(1).replaceAll("<.*?>", "");
       // Use the cleaned description content as needed
   }