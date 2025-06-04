"""
ATENÇÃO: EVITE MODIFICAR ESTE ARQUIVO!

Carrega os nomes principais do módulo lox.
"""

from .ast import Expr, Stmt, Value
from .ctx import Ctx
from .parser import lex, parse, parse_cst, parse_expr
from .node import Node
from .errors import SemanticError

__all__ = [
    "Ctx",
    "eval",
    "Expr",
    "lex",
    "Node",
    "parse_cst",
    "parse",
    "parse_expr",
    "Stmt",
    "SemanticError",
]


def eval(src: str, env: Ctx | dict[str, Value] | None = None) -> Ctx:
    """
    Avalia o código fonte e retorna o ambiente resultante.
    """
    if env is None:
        env = Ctx()
    elif not isinstance(env, Ctx):
        env = Ctx.from_dict(env)
    ast = parse(src)

    try:
        return ast.eval(env)
    except Exception as e:
        print(f"Programa terminou com um erro: {e}")
        print("Variáveis:", env)
        raise
