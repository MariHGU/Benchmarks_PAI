# Ruby
def factorial(n)
  return 1 if n == 0
  (1..n).reduce(:*) # Using range and reduce method
end

# Alternative implementation with recursion
def factorial_recursive(n)
  return 1 if n == 0
  n * factorial_recursive(n - 1)
end