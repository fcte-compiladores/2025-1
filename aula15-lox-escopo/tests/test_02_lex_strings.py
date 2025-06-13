import pytest
from lark import ParseError, Token, UnexpectedCharacters

from lox import parse_expr
from lox.ast import Literal

good_strings = {
    r'""': "",
    r'"foo bar"': "foo bar",
    r'"foo\nbar"': "foo\\nbar",
    '"foo\nbar"': "foo\nbar",
}
bad_strings = [
    r'"escaped \""',
    r"'single quotes'",
    r'"never closes',
    r'"""triple quotes"""',
]


def test_convert_string_to_literal_value():
    ast = parse_expr('"string"')
    if isinstance(ast, Token):
        msg = "Precisa implementar o método def STRING(self, token) no LoxTransformer que converte o token para um Literal(str)"
        raise ValueError(msg)
    if isinstance(ast, str):
        msg = "Converta para Literal(str) e não diretamente para str"
        raise ValueError(msg)
    assert isinstance(ast, Literal)

    if ast.value == '"string"':
        msg = "Não esqueça de remover as aspas do valor da string"
        raise ValueError(msg)

    assert ast.value == "string"


@pytest.mark.parametrize("src, expected", good_strings.items())
def test_good_strings(src: str, expected: str):
    ast = parse_expr(src)
    assert isinstance(ast, Literal)
    assert ast.value == expected


@pytest.mark.parametrize("src", bad_strings)
def test_bad_strings(src):
    with pytest.raises((ParseError, UnexpectedCharacters)):
        parse_expr(src)
