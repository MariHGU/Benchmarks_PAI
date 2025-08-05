String xmlInput = "<xml> ... <description>Example:Description:<THIS-IS-PART-OF-DESCRIPTION></description> ... </xml>";
// Replace any tags inside the description with their escaped equivalents
String cleanedXml = xmlInput.replaceAll("<(/?)(\\w+)>", "&lt;$1$2&gt;");