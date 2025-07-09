"""
ATENÇÃO: EVITE MODIFICAR ESTE ARQUIVO!

Esse módulo usa a biblioteca `argparse` para criar uma interface de linha de comando
(CLI) para o compilador de Lox.

Ele permite que o usuário execute o compilador com diferentes opções, como especificar
o arquivo de entrada, ativar o modo para imprimir as árvores
sintáticas, lexer, etc.

Argparse talvez não seja a melhor opção para criar uma CLI, mas é uma biblioteca
padrão do Python e não requer instalação de dependências externas.
"""

import argparse


from .parser import lex, parse, parse_cst
from . import eval as lox_eval


def make_argparser():
    parser = argparse.ArgumentParser(description="Compilador Lox")
    parser.add_argument(
        "file",
        help="Arquivo de entrada",
    )
    parser.add_argument(
        "-t",
        "--ast",
        action="store_true",
        help="Imprime a árvore sintática.",
    )
    parser.add_argument(
        "-l",
        "--lex",
        action="store_true",
        help="Imprime o lexer.",
    )
    parser.add_argument(
        "-c",
        "--cst",
        action="store_true",
        help="Imprime a árvore sintática concreta produzida pelo Lark.",
    )
    return parser


def main():
    """
    Função principal que cria a interface de linha de comando (CLI) para o compilador Lox.
    """
    parser = make_argparser()
    args = parser.parse_args()

    # Lê arquivo de entrada
    try:
        with open(args.file, "r") as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Arquivo {args.file} não encontrado.")
        exit(1)

    if not args.ast and not args.cst and not args.lex:
        lox_eval(source)
    else:
        debug_source(source, args)


def debug_source(source: str, args):
    """
    Mostra informações de depuração sobre o código Lox passado como argumento.
    """
    if args.ast:
        ast = parse(source)
        print(ast.pretty())

    if args.cst:
        cst = parse_cst(source)
        print(cst.pretty())

    if args.lex:
        for token in lex(source):
            print(f"{token.type}: {token.value}")
