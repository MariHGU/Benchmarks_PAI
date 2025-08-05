def factorial(n)
  return 1 if n == 0
  (1..n).reduce(:*)
end

# Usage:
puts factorial(5) # Output: 120