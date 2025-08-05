#include <vector>
#include <numeric>

double sum_of_squares(const std::vector<double>& numbers) 
{
    return std::accumulate(numbers.begin(), numbers.end(), 0.0,
        [](double acc, double n) { return acc + n * n; });
}