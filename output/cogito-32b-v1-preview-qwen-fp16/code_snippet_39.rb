def calculate_sum(n)
  return 0 if n <= 0
  (1..n).sum
end

# Alternative manual implementation
def calculate_sum_manual(n)
  sum = 0
  for i in 1..n do
    sum += i
  end
  sum
end