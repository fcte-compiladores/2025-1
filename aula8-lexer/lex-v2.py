import re
from rich import print
from typing import Iterator, cast
from dataclasses import dataclass

exemplos_corretos = ["aAa 42 3.14", "aa bbAB #foo\naaa", "aabbbaaa"]
exemplos_incorretos = ["ccc", "a b c", "a c b"]

PATTERNS = {
    "COMMENT": r"#[^\n]*",
    "FLOAT": r"-?0|[1-9][0-9]*\.[0-9]+",
    "INT": r"-?0|[1-9][0-9]*",
    "WA": r"[aA]+",
    "WB": r"[bB]+",
    "WS": r"\s+",
    
    # Importante! Esse deve ser o último padrão para
    # capturar o que os outros padrões não detectaram.
    "ERROR": r".",
}
GROUPS = (f"(?P<{name}>{regex})" for name, regex in PATTERNS.items())
REGEX = "|".join(GROUPS)
LEXER = re.compile(REGEX)


@dataclass
class Token:
    kind: str
    word: str


def tokenizer(src: str) -> Iterator[Token]:
    IGNORE = ("WS","COMMENT")
    
    for m in LEXER.finditer(src):
        kind = cast(str, m.lastgroup)
        word = m.group(0)
        if kind == "ERROR":
            raise SyntaxError(m)
        if kind in IGNORE:
            continue
        
        yield Token(kind, word)
    

if __name__ == "__main__":
    print("[blue bold]CORRETOS")
    for src in exemplos_corretos:
        print(f"{src =}")
        for token in tokenizer(src):
            print(f" - {token}")
        
    print("\n[red bold]INCORRETOS")
    for src in exemplos_incorretos:
        try:
            tokens = list(tokenizer(src))
        except SyntaxError:
            print(f"{src =} OK!")
        else:
            print(f"{src =}")
            print(f"{tokens =}\n")
