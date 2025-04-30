from rich import print
from typing import cast
import re

exemplos_corretos = ["aAa", "bbBBB", "bb  AA  \t bbBbB \n AaaAa"]
exemplos_invalidos = ["ccc"]

Token = tuple[str, str]

LEXER = re.compile(r"(?P<AWORD>[aA]+)|(?P<BWORD>[bB]+)|(?P<WS>\s+)")


def lexer(src: str) -> list[Token]:
    result: list[Token] = []
    
    pos = 0
    while True:
        m = LEXER.match(src, pos)
        if m is None:
            raise SyntaxError(src[pos:])
        
        initial, end = m.span()
        token = (src[initial:end], cast(str, m.lastgroup))
        result.append(token)
        pos = end
        
        if pos == len(src):
            return result 
        


if __name__ == "__main__":
    print("EXEMPLOS CORRETOS")
    for exemplo in exemplos_corretos:
        print(f"> {exemplo}")
        print(f"[green]- {lexer(exemplo)}\n")

    print("EXEMPLOS INCORRETOS")
    for exemplo in exemplos_invalidos:
        print(">", exemplo)
        try:
            out = lexer(exemplo)
        except SyntaxError:
            print("[green]OK!")
        else:
            print("[red]aceitou e retornou", out)