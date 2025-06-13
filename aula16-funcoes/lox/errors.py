"""
ATENÇÃO: EVITE MODIFICAR ESTE ARQUIVO!

Execeções usadas no compilador Lox.
"""

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .ast import Value


class SemanticError(Exception):
    """
    Exceção para erros semânticos.
    """

    def __init__(self, msg, token=None):
        super().__init__(msg)
        self.token = token


class ForceReturn(Exception):
    """
    Exceção que serve para forçar uma função a retornar durante a avaliação
    da mesma.
    """

    def __init__(self, value: "Value"):
        self.value = value
        super().__init__(self.value)
