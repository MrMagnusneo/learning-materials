#include <iostream>
#include <iomanip>
#include <ctime>
using namespace std;

bool isPrime(int num) {
    if (num <= 1) return false;
    if (num == 2) return true;
    if (num % 2 == 0) return false;

    for (int i = 3; i * i <= num; i += 2) {
        if (num % i == 0) return false;
    }
    return true;
}


int main(){
    clock_t start_tick, end_tick; double time;
    int prime, number, count = 0; cout << "Input the prime number: "; cin >> prime; cout << "\n";
    start_tick = clock();

    for (number = 2; count < prime; number++){
        if (isPrime(number)) count++;
        if (count == prime) break;
    }

    end_tick = clock();
    time = (double)(end_tick - start_tick) / CLOCKS_PER_SEC;
    cout << "Prime number " << prime << ": " << number << "\n";
    cout << "Calculation time: " << fixed << time << " seconds\n";
}