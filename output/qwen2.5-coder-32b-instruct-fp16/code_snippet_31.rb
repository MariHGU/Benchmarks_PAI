def factorial(n)
  return 1 if n == 0
  (1..n).reduce(1) { |acc, i| acc * i }
end

puts factorial(5)  # Output: 120