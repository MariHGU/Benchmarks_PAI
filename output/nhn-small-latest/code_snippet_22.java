// Example pattern matching <description> contents and escaping tags
   String cleanedDescription = originalDescription.replaceAll("<[^>]+>", "&lt;$0&gt;");