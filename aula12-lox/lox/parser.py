"""
ATENÇÃO: EVITE MODIFICAR ESTE ARQUIVO!

Define a gramática da Linguagem e funções para realizar a análise sintática,
análise léxica, etc.
"""

from pathlib import Path
from typing import Iterator
from lark import Lark, Token, Tree

from .transformer import LoxTransformer
from .ast import Program, Expr


DIR = Path(__file__).parent
GRAMMAR_PATH = DIR / "grammar.lark"


ast_parser = Lark(
    GRAMMAR_PATH.open(),
    transformer=LoxTransformer(),
    parser="lalr",
    start=["start", "expr"],
)
cst_parser = Lark(
    GRAMMAR_PATH.open(),
    parser="lalr",
    start=["start", "expr"],
)


def parse(src: str) -> Program:
    """
    Função que recebe um código fonte e retorna a árvore sintática.

    A função usa o Lark para fazer a análise léxica e sintática do código
    fonte. O resultado é uma árvore sintática que representa a estrutura
    do código usando os nós definidos na classe `Node`.

    Args:
        src (str):
            Código fonte a ser analisado.
        semantic_check (bool):
            Se True (padrão) realiza a análise semântica do código.
    """
    tree = ast_parser.parse(src, start="start")
    assert isinstance(tree, Program), f"Esperava um Program, mas recebi {type(tree)}"
    tree.validate_tree()
    tree.desugar_tree()
    return tree


def parse_expr(src: str) -> Expr:
    """
    Função que recebe um código fonte e retorna a árvore sintática
    representando uma expressão.

    Similar à função `parse`, mas analisa o código como se fosse
    apenas uma expressão. Isso é útil para avaliar expressões
    isoladas, sem a necessidade de um bloco de código completo. Isto também
    facilita o teste de expressões individuais.

    Args:
        src (str):
            Código fonte a ser analisado.
        semantic_check (bool):
            Se True (padrão) realiza a análise semântica do código.

    Examples:
        >>> parse_expr("1 + 2")
        BinOp(left=Literal(value=1), right=Literal(value=2), op=op.add)
        >>> ctx = Ctx()
        >>> parse_expr("1 + 2 * 3").eval(Ctx())
        7
    """
    tree = ast_parser.parse(src, start="expr")
    assert isinstance(tree, Expr), f"Esperava um Expr, mas recebi {type(tree)}"
    tree.validate_tree()
    tree.desugar_tree()
    return tree


def parse_cst(src: str) -> Tree:
    """
    Similar a função `parse`, mas retorna a árvore sintática produzida pelo
    Lark.

    Não é exatamente a árvore concreta, pois o Lark produz algumas
    simplificações, mas é próxima o suficiente.

    Args:
        src (str):
            Código fonte a ser analisado.
        expr (bool):
            Se True, analisa o código como se fosse apenas uma expressão.
    """
    return cst_parser.parse(src, start="start")  # type: ignore


def lex(src: str) -> Iterator[Token]:
    """
    Retorna um iterador sobre os tokens do código fonte.
    """
    return ast_parser.lex(src)
