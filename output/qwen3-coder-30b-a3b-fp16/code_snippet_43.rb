def factorial(n)
  if n < 0
    raise ArgumentError, "Factorial is not defined for negative numbers"
  elsif n == 0 || n == 1
    1
  else
    n * factorial(n - 1)
  end
end

# Usage
puts factorial(5)  # Output: 120