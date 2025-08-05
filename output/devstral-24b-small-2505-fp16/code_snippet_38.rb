def sum_positive_numbers(arr)
  arr.select { |num| num > 0 }.reduce(0, :+)
end