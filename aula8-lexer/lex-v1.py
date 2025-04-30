import re
from rich import print
from typing import cast

exemplos_corretos = ["aAa", "aa bbAB", "aabbbaaa"]
exemplos_incorretos = ["ccc", "a b c", "a c b"]

LEXER = re.compile(r"(?P<WA>[aA]+)|(?P<WB>[bB]+)|(?P<WS>\s+)|(?P<ERROR>.)")
Token = tuple[str, str]



def tokenizer(src: str) -> list[Token]:
    result = []
    
    for m in LEXER.finditer(src):
        kind = cast(str, m.lastgroup)
        word = m.group(0)
        if kind == "ERROR":
            raise SyntaxError(m)
        if kind == "WS":
            continue
        
        result.append((kind, word))
    
    return result 


if __name__ == "__main__":
    print("[blue bold]CORRETOS")
    for src in exemplos_corretos:
        tokens = tokenizer(src)
        print(f"{src =}")
        print(f"{tokens =}\n")
        
    print("[red bold]INCORRETOS")
    for src in exemplos_incorretos:
        try:
            tokens = tokenizer(src)
        except SyntaxError:
            print(f"{src =} OK!")
        else:
            print(f"{src =}")
            print(f"{tokens =}\n")
