from __future__ import annotations
from math import sqrt
from time import time
from typing import TYPE_CHECKING, cast


if TYPE_CHECKING:
    from .ast import Value


def read_number(msg: str) -> float:
    try:
        return float(input(msg))
    except ValueError:
        print("Digite um número válido!")
        return read_number(msg)


BUILTINS = {
    "clock": time,
    "sqrt": sqrt,
    "max": max,
    "read_number": read_number,
    "is_even": lambda n: n % 2 == 0.0,
}


class Ctx:
    """
    Contexto de execução. Por enquanto é só um dicionário que armazena nomes
    das variáveis e seus respectivos valores.
    """

    def __init__(self, globals: dict | None = None , parent: Ctx | None = None):
        if globals is None:
            globals = {}
        self.env = globals
        self.parent = parent

    @classmethod
    def from_dict(cls, global_env: dict[str, Value]) -> Ctx:
        """
        Cria um novo contexto a partir de um dicionário.
        """
        builtins = cls(BUILTINS, None)
        return cls(global_env, builtins)

    def __getitem__(self, key: str) -> Value:
        """
        self[key] <==> self.__getitem__(key)
        """
        if key in self.env:
            return self.env[key]
        if self.parent is None:
            raise KeyError(key)
        return self.parent[key]

    def __setitem__(self, key: str, value: Value):
        """
        self[key] = value <==> self.__setitem__(key, value)
        """
        if key in self.env:
            self.env[key] = value
            return
        if self.parent is None:
            raise KeyError(key)
        self.parent[key] = value

    def var_def(self, key: str, value: Value):
        """
        Declara uma nova variável.
        """
        self.env[key] = value

    def pop(self) -> tuple[dict, Ctx]:
        """
        Remove o último dicionário da pilha
        """
        return (self.env, cast(Ctx, self.parent))

    def push(self, env: dict) -> Ctx:
        """
        Coloca um novo dicionário no topo da pilha e retorna o contexto
        correspondente.
        """
        return Ctx(env, self)


class CtxAlt:
    """
    Contexto de execução. Por enquanto é só um dicionário que armazena nomes
    das variáveis e seus respectivos valores.
    """

    def __init__(self, globals: dict | None = None):
        if globals is None:
            globals = {}
        self._stack = [BUILTINS, globals]

    @classmethod
    def from_dict(cls, env: dict[str, Value]) -> CtxAlt:
        """
        Cria um novo contexto a partir de um dicionário.
        """
        return cls(env)

    def __getitem__(self, key: str) -> Value:
        for env in reversed(self._stack):
            if key in env:
                return env[key]
        raise KeyError(key)

    def __setitem__(self, key: str, value: Value):
        for env in reversed(self._stack):
            if key in env:
                env[key] = value
        raise KeyError(key)

    def var_def(self, key: str, value: Value):
        """
        Declara uma nova variável.
        """
        env = self._stack[-1]
        env[key] = value

    def pop(self):
        """
        Remove o último dicionário da pilha
        """
        return self._stack.pop()

    def push(self, env: dict):
        """
        Coloca um novo dicionário no topo da pilha
        """
        self._stack.append(env)
