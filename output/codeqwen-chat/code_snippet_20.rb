def compare_languages(string1, string2)
  return "Ruby" if string1 == string2
  return "Python" if string1 == string2[::-1]
  return "C++" if string1[0..-2] == string2 && string1[-1] != string2[-1]
  return "Java" if string1.chars.reverse == string2.chars
end

puts compare_languages("Hello", "olleH") # => "Ruby"
puts compare_languages("Hello", "olleh") # => "Python"
puts compare_languages("Hell", "llHe")   # => "C++"
puts compare_languages("Hello", "olleo") # => "Java"