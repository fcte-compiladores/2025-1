"""
Implementa o transformador da árvore sintática que converte entre as representações

    lark.Tree -> lox.ast.Node.

A resolução de vários exercícios requer a modificação ou implementação de vários
métodos desta classe.
"""

from typing import Callable
from lark import Transformer, v_args

from . import runtime as op
from .ast import *


def op_handler(op: Callable):
    """
    Fábrica de métodos que lidam com operações binárias na árvore sintática.

    Recebe a função que implementa a operação em tempo de execução.
    """

    def method(self, left, right):
        return BinOp(left, right, op)

    return method


@v_args(inline=True)
class LoxTransformer(Transformer):
    # Programa
    def program(self, *stmts):
        return Program(list(stmts))

    # Operações matemáticas básicas
    mul = op_handler(op.mul)
    div = op_handler(op.truediv)
    sub = op_handler(op.sub)
    add = op_handler(op.add)

    # Comparações
    gt = op_handler(op.gt)
    lt = op_handler(op.lt)
    ge = op_handler(op.ge)
    le = op_handler(op.le)
    eq = op_handler(op.eq)
    ne = op_handler(op.ne)

    # Outras expressões
    def call(self, name: Var, params: list):
        return Call(name.name, params)

    def params(self, *args):
        params = list(args)
        return params

    # Comandos
    def block(self, *stmts: Stmt):
        return Block(list(stmts))
    
    def assign(self, var: Var, value: Expr):
        return Assign(var.name, value)
    
    def setattr(self, target: Expr, attr: Var, value: Expr):
        return Setattr(target, attr.name, value)

    # Declarações
    def var_def(self, var: Var, value: Expr):
        return VarDef(var.name, value)

    def fun_def(self, name: Var, args: list[str], body: Block):
        return Function(name.name, args, body.stmts)
    
    def fun_args(self, *args: Var):
        return [var.name for var in args]

    # Comandos
    def return_cmd(self, expr: Expr | None = None):
        if expr is None:
            expr = Literal(None)
        return Return(expr)

    def print_cmd(self, expr: Expr) -> Print:
        return Print(expr)
    
    def if_cmd(self, cond: Expr, then: Stmt, orelse: Stmt = Block([])):
        return If(cond, then, orelse)
    
    def while_cmd(self, cond: Expr, body: Stmt):
        return While(cond, body)
        
    def for_cmd(self, for_args: tuple, body: Stmt):
        """
        Fazemos a transformação (desugar)
        
        De:
            for (init; cond; incr) body

        Para:
            {
                init
                while (cond) {
                    body;
                    incr;
                }
            }
        """
        init, cond, incr = for_args
        return Block([
            init,
            While(cond, Block([
                body,
                incr,
            ]))
        ])
    
    def for_args(self, arg1, arg2, arg3):
        return (arg1, arg2, arg3)
    
    def opt_expr(self):
        return Literal(True)

    def VAR(self, token) -> Var:
        name = str(token)
        return Var(name)

    def NUMBER(self, token) -> Literal:
        num = float(token)
        return Literal(num)

    def STRING(self, token) -> Literal:
        text = str(token)[1:-1]
        return Literal(text)

    def NIL(self, _) -> Literal:
        return Literal(None)

    def BOOL(self, token) -> Literal:
        return Literal(token == "true")
