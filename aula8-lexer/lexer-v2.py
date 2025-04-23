from rich import print
from typing import Iterator, cast
import re

exemplos_corretos = ["aAa", "bbBBB", "bb  AA  \t bbBbB \n AaaAa"]
exemplos_invalidos = ["ccc"]

Token = tuple[str, str]

NON_TERMINALS = {
    "AWORD": r"[aA]+",
    "BWORD": r"[bB]+",
    "WS": r"\s+",
    # Importante! Erro deve ser o último do dicionário
    "ERROR": r".",
}
PATTERNS = (f"(?P<{name}>{pattern})" for name, pattern in NON_TERMINALS.items())
REGEX = "|".join(PATTERNS)
LEXER = re.compile(REGEX)


def lexer(src: str) -> list[Token]:
    return list(iter_tokens(src))
        
        
def iter_tokens(src: str) -> Iterator[Token]:
    for m in LEXER.finditer(src):
        # Ignora os espaços (WS)
        if m.lastgroup == "WS":
            continue
        if m.lastgroup == "ERROR":
            pos = m.pos
            chr = m.group()
            raise SyntaxError(f"caractere inválido em {pos}: {chr}")
        
        yield (m.group(0), cast(str, m.lastgroup))
 


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