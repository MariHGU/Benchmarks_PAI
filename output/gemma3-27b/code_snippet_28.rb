def factorial(n)
  if n == 0
    1
  else
    n * factorial(n - 1)
  end
end

# Example usage:
puts factorial(5) # Output: 120