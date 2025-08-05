String input = "<xml><description>Example:Description:<THIS-IS-PART-OF-DESCRIPTION></description></xml>";
Pattern pattern = Pattern.compile("(?<=\\<description\\>).*?(?=\\</description\\>)"); // Finds content within <description> tags
Matcher matcher = pattern.matcher(input);
StringBuffer buffer = new StringBuffer();
while (matcher.find()) {
    String descriptionContent = matcher.group().replace("<", "&lt;").replace(">", "&gt;"); // Replace "<" and ">" characters with their XML entities
    matcher.appendReplacement(buffer, ""); // Remove the found content from input string
    buffer.append(descriptionContent); // Append escaped description content to buffer
}
matcher.appendTail(buffer); // Add remaining parts of input string to buffer
String cleanedInput = buffer.toString(); // Your final XML input as a string without nested tags inside <description> tag