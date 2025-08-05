def factorial(n)
  return 1 if n <= 1
  n * factorial(n - 1)
end

puts "Factorial of 5 is #{factorial(5)}"