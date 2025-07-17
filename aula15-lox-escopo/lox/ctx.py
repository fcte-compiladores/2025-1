from __future__ import annotations
from math import sqrt
from time import time
from types import MappingProxyType
from typing import TYPE_CHECKING, MutableMapping, TypeVar, cast


if TYPE_CHECKING:
    from .ast import Value

def read_number(msg: str) -> float:
    try:
        return float(input(msg))
    except ValueError:
        print("Digite um número válido!")
        return read_number(msg)

STD_LIB = {
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
    
    def __init__(self, env: dict, parent: Ctx | None = None):
        self.env = env
        self.parent = parent
        
    @classmethod
    def from_dict(cls, env: dict[str, "Value"]) -> "Ctx":
        """
        Cria um novo contexto a partir de um dicionário.
        """
        stdlib = Ctx(STD_LIB)
        return cls(env, stdlib)

    def pop(self) -> tuple[dict, "Ctx"]:
        """
        Remove o dicionário do topo da pilha, retornando-o.
        """
        return self.env, self.parent
    
    def push(self, env: dict) -> "Ctx":
        """
        Coloca dicionário no topo da pilha.
        """
        return Ctx(env, self)

    def get(self, item):
        return self[item]
        
    def var_def(self, name: str, value: "Value"):
        self.env[name] = value

    def __getitem__(self, item):
        if item in self.env:
            return self.env[item]
        return self.parent[item]
        
    def __setitem__(self, item, value):
        if item in self.env:
            self.env[item] = value
        else:
            self.parent[item] = value
        

class Ctx2:
    """
    Contexto de execução. Por enquanto é só um dicionário que armazena nomes
    das variáveis e seus respectivos valores.
    """
    
    def __init__(self):
        self.stack = [STD_LIB, {}]
        
    @classmethod
    def from_dict(cls, env: dict[str, "Value"]) -> "Ctx":
        """
        Cria um novo contexto a partir de um dicionário.
        """
        new = cls()
        new.stack.append(env)
        return new

    def pop(self) -> dict:
        """
        Remove o dicionário do topo da pilha, retornando-o.
        """
        return self.stack.pop()
    
    def push(self, env: dict):
        """
        Coloca dicionário no topo da pilha.
        """
        self.stack.append(env)

    def get(self, item):
        return self.get(item)
        
    def var_def(self, name: str, value: "Value"):
        tos = self.stack[-1]
        tos[name] = value

    def __getitem__(self, item):
        for env in reversed(self.stack):
            if item in env:
                return env[item]
        raise KeyError(item)
    
    def __setitem__(self, item, value):
        for env in reversed(self.stack):
            if item in env:
                env[item] = value
                return
        raise KeyError(item)
    
        