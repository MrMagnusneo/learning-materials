#include <iostream>
#include <iomanip>
#include <vector>
#include <ctime>
#include <boost/multiprecision/cpp_int.hpp>
using namespace std;

int main(){
    srand(time(0));
    clock_t start_tick, end_tick; double time;
    int count; cout << "Input how much coin will flip: "; cin >> count; cout << "\n";
    int head = 0; int tail = 0;
    start_tick = clock();

    for (int i = 0; i < count; i++){
        if (rand()%2==0) head++;
        else tail++;
    }

    end_tick = clock();
    time = (double)(end_tick - start_tick) / CLOCKS_PER_SEC;
    cout << "Head probability: " << (static_cast<double>(head) / count) * 100 << "\nHead counts: " << head << "\n";
    cout << "Tail probability: " << (static_cast<double>(tail) / count) * 100 << "\nTail counts: " << tail << "\n";
    cout << "Calculation time: " << fixed << time << " seconds\n";
}