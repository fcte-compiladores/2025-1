from typing import Callable, Union
from dataclasses import dataclass
from pathlib import Path
import operator

from lark import Lark, Transformer, v_args

DIR = Path(__file__).parent
GRAMMAR_PATH = DIR / "grammar.lark"
grammar = GRAMMAR_PATH.read_text()


def op_handler(op):
    def method(self, left, right):
        return BinOp(left, right, op)
    return method


@v_args(inline=True)
class LoxTransformer(Transformer):
    # Operações matemáticas básicas
    mul = op_handler(operator.mul)
    div = op_handler(operator.truediv)
    sub = op_handler(operator.sub)
    add = op_handler(operator.add)
    
    # Comparações
    gt = op_handler(operator.gt)
    lt = op_handler(operator.lt)
    ge = op_handler(operator.ge)
    le = op_handler(operator.le)
    eq = op_handler(operator.eq)
    ne = op_handler(operator.ne)
    
    
    def VAR(self, token):
        name = str(token)
        return Var(name)

    def NUMBER(self, token):
        num = float(token)
        return Literal(num)

transformer = LoxTransformer()
parser = Lark(grammar)

# Tipos válidos para expressões na árvore sintática
Expr = Union["BinOp", "Literal", "Var"]

# Comandos na árvore sintática
Stmt = Union["If", "For", "While"]

# Tipos de valores que podem aparecer durante a execução do programa
Value = bool | str | float | None

# Contexto de execução
Ctx = dict[str, Value]


@dataclass
class BinOp:
    """
    Uma operação infixa com dois operandos. x + y, 2 * x, etc.
    """

    left: Expr
    right: Expr
    op: Callable[[Value, Value], Value]
    
    def eval(self, ctx: Ctx):
        left_value = self.left.eval(ctx)
        right_value = self.right.eval(ctx)
        return self.op(left_value, right_value)


@dataclass
class Literal:
    """
    Representa valores literais no código, ex.: strings, booleanos,
    números, etc.
    """

    value: Value
    
    def eval(self, ctx: Ctx):
        return self.value


@dataclass
class Var:
    """
    Uma variável no código
    """

    name: str
    
    def eval(self, ctx: Ctx):
        try:
            return ctx[self.name]
        except KeyError:
            raise NameError(f"variável {self.name} não existe!")


@dataclass
class If: ...


@dataclass
class For: ...


@dataclass
class While:
    cond: Expr
    body: list[Stmt]


def pprint(obj):
    if hasattr(obj, "pretty"):
        print(obj.pretty())
    else:
        print(obj)


if __name__ == "__main__":
    src = "2 * x + y > 40"

    print("src:", src)
    lark_tree = parser.parse(src)
    lox_tree = transformer.transform(lark_tree)
    print("-" * 10)
    result = lox_tree.eval({"x": 20, "y": 2, "z": 3})
    pprint(result)
