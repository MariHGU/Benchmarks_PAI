Pattern pattern = Pattern.compile("<description>(.*?)</description>", Pattern.DOTALL);
Matcher matcher = pattern.matcher(xml);
while(matcher.find()) {
    String descriptionContent = matcher.group(1);
    // Handle the content here
}