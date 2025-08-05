# Ruby
def factorial(n)
  return nil if n < 0
  result = 1
  (1..n).each do |i|
    result *= i
  end
  result
end