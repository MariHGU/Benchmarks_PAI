def factorial(n)
  return 1 if n == 0
  (1..n).reduce(:*)
end

# Example usage
puts factorial(5)  # Output: 120