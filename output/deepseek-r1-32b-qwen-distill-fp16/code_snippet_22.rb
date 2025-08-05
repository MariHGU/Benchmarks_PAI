def sum_of_even_squares(n)
    sum = 0
    (1..n).each do |num|
        if num.even?
            sum += num ** 2
        end
    end
    sum
end

puts sum_of_even_squares(4) # Output: 20