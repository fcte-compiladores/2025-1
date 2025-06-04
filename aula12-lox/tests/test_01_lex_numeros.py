import re

import pytest

MY_NUMBER_RE = re.compile(r"([1-9][0-9]*|0)(\.[0-9]+)?")
LOX_NUMBER_RE = re.compile(r"[0-9]+(\.[0-9]+)?")


@pytest.fixture
def mod(mod_loader):
    """
    Fixture para o módulo que contém as expressões regulares.
    """
    return mod_loader("01-lex_numeros")


def test_valid_in_both(mod):
    examples = mod.VALIDOS_EM_AMBAS_ESPECIFICACOES
    common_test(examples, lox=True, ours=True)
    msg = "Você precisa adicionar cinco exemplos ou mais"
    assert len(examples) >= 5, msg


def test_valid_in_lox_only(mod):
    examples = mod.VALIDOS_EM_LOX_E_INVALIDOS_NA_NOSSA_VERSAO
    common_test(examples, lox=True, ours=False)
    msg = "Você precisa adicionar cinco exemplos ou mais"
    assert len(examples) >= 5, msg


def test_valid_in_ours_only(mod):
    examples = mod.VALIDOS_NA_NOSSA_VERSAO_E_INVALIDOS_EM_LOX
    common_test(examples, lox=False, ours=True)
    assert len(examples) == 0, "Nossa versão somente aceita números Lox válidos."


def common_test(exemplos: list[str], lox=bool, ours=bool):
    def should(expect: bool):
        return "deveria" if expect else "não deveria"

    def check(expect: bool, example: str, regex: re.Pattern):
        if expect:
            return regex.fullmatch(example)
        return not regex.fullmatch(example)

    print(f"{exemplos=}")
    for n, ex in enumerate(exemplos, start=0):
        assert isinstance(
            ex, str
        ), f"[{n}] escreva exemplos como strings: {exemplos[n]=}"

        msg = f"resposta[{n}]={ex!r} {should(ours)} ser aceito na nossa versão"
        assert check(ours, ex, MY_NUMBER_RE), msg

        msg = f"resposta[{n}]={ex!r} {should(lox)} ser aceito em lox"
        assert check(lox, ex, LOX_NUMBER_RE), msg

    repeated = set()
    for ex in exemplos:
        assert ex not in repeated, f"exemplo repetido: {ex}"
        repeated.add(ex)
