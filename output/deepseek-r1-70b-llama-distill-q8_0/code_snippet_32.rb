def sum_even_numbers(array)
    array.select { |num| num.even? }.sum
end