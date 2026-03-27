#include <iostream>
#include <iomanip>
#include <ctime>
#include <boost/multiprecision/cpp_int.hpp>
using namespace std;
using namespace boost::multiprecision;

int main(){
    clock_t start_tick, end_tick; double time;
    int count; cout << "Input the fib number: "; cin >> count; cout << "\n";
    cpp_int a = 0, b = 1, next;
    start_tick = clock();

    if (count == 0) b = 0;
    else if (count == 1) b = 1;
    else{
    for (int i = 2; i < count; i++){
        next = a + b;
        a = b;
        b = next;
    }}
    end_tick = clock();
    time = (double)(end_tick - start_tick) / CLOCKS_PER_SEC;
    cout << "Fib number " << count << ": " << b << "\n";
    cout << "Calculation time: " << fixed << time << " seconds\n";
}
