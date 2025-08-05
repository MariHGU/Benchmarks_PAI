def factorial(n)
  return 1 if n == 0
  n * factorial(n - 1)
end

# Example usage:
puts factorial(5) # Output: 120