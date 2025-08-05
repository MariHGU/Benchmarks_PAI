def factorial(n)
  return 1 if n == 0 || n == 1
  n * factorial(n - 1)
end

puts factorial(5) # Output: 120