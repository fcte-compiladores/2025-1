#!/usr/bin/python3
import sys
import click  # pip3 install click/apt install python3-click

c_template = """
#include<stdio.h>

int main() {
    char memory[10000];
    int index = 0;

    for (int i=0; i < 10000; i++) {
        memory[i] = 0;
    }
"""


class BF:
    def __init__(self):
        self.lines = []
        
    def run(self, src: str):
        chars = iter(src)
        for c in chars:
            match c:
                case ">":
                    print("    index += 1;")
                case "<":
                    print("    index -= 1;")
                case "+":
                    print("    memory[index]++;")
                case "-":
                    print("    memory[index]--;")
                case ".":
                    print('    printf("%c", memory[index]);')
                case ",":
                    print('    memory[index] = getchar(); fflush(stdin);')
                case "[":
                    print("    while(memory[index] != 0) {")
                case "]":
                    print("    }")


def main():
    vm = BF()
    filename = sys.argv[-1]
    
    with open(filename, "r") as fd:
        source = fd.read()

    print(c_template)
    vm.run(source)
    print("   return 0;")
    print("}")


if __name__ == "__main__":
    main()