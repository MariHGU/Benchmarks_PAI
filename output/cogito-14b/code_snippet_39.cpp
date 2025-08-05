#include <iostream>
using namespace std;

void print_hello_and_numbers() {
    cout << "Hello, World!" << endl;
    for (int i = 1; i <= 5; i++) {
        cout << i << endl;
    }
}

// Call the function
int main() {
    print_hello_and_numbers();
    return 0;
}