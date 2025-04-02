
#include<stdio.h>

int main() {
    char memory[10000];
    int index = 0;

    for (int i=0; i < 10000; i++) {
        memory[i] = 0;
    }

    memory[index]--;
    index += 1;
    memory[index]++;
    index -= 1;
   return 0;
}
