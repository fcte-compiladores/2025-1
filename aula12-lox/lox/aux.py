lambda x, y, z: x + y 

def f(x: str) -> int:
    return "not an int"


def compilador(src: str) -> str | bytes:
    tokens = lex(src) # análise léxica
    ast = parse(tokens)   # análise sintática
    IR = analysis(ast)   # análise semântica
    IR = optimize(IR)   # otimização
    code = codegen(IR)    # geração de código
    return code


def __getattr__(attr):
    ...