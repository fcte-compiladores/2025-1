from abc import ABC
from dataclasses import dataclass
from typing import Callable, Iterable
from types import FunctionType
from bytecode import Bytecode, Instr, Compare, Label

from . import runtime as ops
from .ctx import Ctx

# Declaramos nossa classe base num módulo separado para esconder um pouco de
# Python relativamente avançado de quem não se interessar pelo assunto.
#
# A classe Node implementa um método `pretty` que imprime as árvores de forma
# legível. Também possui funcionalidades para navegar na árvore usando cursores
# e métodos de visitação.
from .node import Node


#
# TIPOS BÁSICOS
#

# Tipos de valores que podem aparecer durante a execução do programa
Value = bool | str | float | None | Callable


class Expr(Node, ABC):
    """
    Classe base para expressões.

    Expressões são nós que podem ser avaliados para produzir um valor.
    Também podem ser atribuídos a variáveis, passados como argumentos para
    funções, etc.
    """

    is_expr = True
    is_stmt = False

    def emit_instructions(self) -> Iterable[Instr | Label]:
        msg = f"{self.__class__.__name__}.emit_instructions() não implementado"
        raise NotImplementedError(msg)


class Stmt(Node, ABC):
    """
    Classe base para comandos.

    Comandos são associdos a construtos sintáticos que alteram o fluxo de
    execução do código ou declaram elementos como classes, funções, etc.
    """

    is_expr = False
    is_stmt = True

    def emit_instructions(self) -> Iterable[Instr | Label]:
        msg = f"{self.__class__.__name__}.emit_instructions() não implementado"
        raise NotImplementedError(msg)


@dataclass
class Program(Node):
    """
    Representa um programa.

    Um programa é uma lista de comandos.
    """

    stmts: list[Stmt]

    def eval(self, ctx: Ctx):
        for stmt in self.stmts:
            stmt.eval(ctx)


#
# EXPRESSÕES
#
@dataclass
class BinOp(Expr):
    """
    Uma operação infixa com dois operandos.

    Ex.: x + y, 2 * x, 3.14 > 3 and 3.14 < 4
    """

    left: Expr
    right: Expr
    op: Callable[[Value, Value], Value]

    OP_TO_INSTR = {
        ops.add: Instr("BINARY_ADD"),
        ops.mul: Instr("BINARY_MULTIPLY"),
        ops.truediv: Instr("BINARY_TRUE_DIVIDE"),
        ops.sub: Instr("BINARY_SUBTRACT"),
        ops.gt: Instr("COMPARE_OP", Compare.GT),
        ops.lt: Instr("COMPARE_OP", Compare.LT),
        ops.ge: Instr("COMPARE_OP", Compare.GE),
        ops.le: Instr("COMPARE_OP", Compare.LE),
        ops.eq: Instr("COMPARE_OP", Compare.EQ),
        ops.ne: Instr("COMPARE_OP", Compare.NE),
    }

    def eval(self, ctx: Ctx):
        left_value = self.left.eval(ctx)
        right_value = self.right.eval(ctx)
        return self.op(left_value, right_value)

    def emit_instructions(self):
        yield from self.left.emit_instructions()
        yield from self.right.emit_instructions()
        yield self.OP_TO_INSTR[self.op]


@dataclass
class Var(Expr):
    """
    Uma variável no código

    Ex.: x, y, z
    """

    name: str

    def eval(self, ctx: Ctx):
        try:
            return ctx[self.name]
        except KeyError:
            raise NameError(f"variável {self.name} não existe!")

    def emit_instructions(self):
        yield Instr("LOAD_FAST", self.name)


@dataclass
class Literal(Expr):
    """
    Representa valores literais no código, ex.: strings, booleanos,
    números, etc.

    Ex.: "Hello, world!", 42, 3.14, true, nil
    """

    value: Value

    def eval(self, ctx: Ctx):
        return self.value

    def emit_instructions(self):
        yield Instr("LOAD_CONST", self.value)


@dataclass
class And(Expr):
    """
    Uma operação infixa com dois operandos.

    Ex.: x and y
    """


@dataclass
class Or(Expr):
    """
    Uma operação infixa com dois operandos.
    Ex.: x or y
    """


@dataclass
class UnaryOp(Expr):
    """
    Uma operação prefixa com um operando.

    Ex.: -x, !x
    """

    op: str
    var: Expr

    operations = {
        "-": "UNARY_NEGATIVE",
        "!": "UNARY_NOT",
    }

    def eval(self, ctx):
        print(self.op, self.var)

    def emit_instructions(self):
        yield from self.var.emit_instructions()
        yield Instr(self.operations[self.op])


@dataclass
class Call(Expr):
    """
    Uma chamada de função.

    Ex.: fat(42)
    """

    name: str
    params: list[Expr]

    def eval(self, ctx: Ctx):
        func = ctx[self.name]
        params = [param.eval(ctx) for param in self.params]

        if callable(func):
            return func(*params)
        raise TypeError(f"{self.name} não é uma função!")

    def emit_instructions(self):
        expr = Var(self.name)
        yield from expr.emit_instructions()
        for param in self.params:
            yield from param.emit_instructions()
        yield Instr("CALL_FUNCTION", len(self.params))


@dataclass
class This(Expr):
    """
    Acesso ao `this`.

    Ex.: this
    """


@dataclass
class Super(Expr):
    """
    Acesso a method ou atributo da superclasse.

    Ex.: super.x
    """


@dataclass
class Assign(Expr):
    """
    Atribuição de variável.

    Ex.: x = 42
    """

    name: str
    value: Expr

    def eval(self, ctx: Ctx):
        key = self.name
        value = self.value.eval(ctx)
        ctx[key] = value
        return value


@dataclass
class Getattr(Expr):
    """
    Acesso a atributo de um objeto.

    Ex.: x.y
    """

    atom: Expr
    attr: str

    def eval(self, ctx):
        return super().eval(ctx)

    def emit_instructions(self):
        yield from self.atom.emit_instructions()
        yield Instr("LOAD_ATTR", self.attr)


@dataclass
class Setattr(Expr):
    """
    Atribuição de atributo de um objeto.

    Ex.: x.y = 42
    """

    target: Expr
    attr: str
    value: Expr

    def eval(self, ctx: Ctx):
        target = self.target.eval(ctx)
        value = self.target.eval(ctx)
        setattr(target, self.attr, value)
        return value


#
# COMANDOS
#
@dataclass
class Print(Stmt):
    """
    Representa uma instrução de impressão.

    Ex.: print "Hello, world!";
    """

    expr: Expr

    def eval(self, ctx: Ctx):
        value = self.expr.eval(ctx)
        print(value)

    def emit_instructions(self):
        yield Instr("LOAD_GLOBAL", "print")
        yield from self.expr.emit_instructions()
        yield Instr("CALL_FUNCTION", 1)
        yield Instr("POP_TOP")


@dataclass
class Return(Stmt):
    """
    Representa uma instrução de retorno.

    Ex.: return x;
    """

    expr: Expr

    def eval(self, ctx: Ctx):
        value = self.expr.eval(ctx)
        raise LoxReturn(value)

    def emit_instructions(self):
        yield from self.expr.emit_instructions()
        yield Instr("RETURN_VALUE")


@dataclass
class VarDef(Stmt):
    """
    Representa uma declaração de variável.

    Ex.: var x = 42;
    """

    name: str
    value: Expr

    def eval(self, ctx: Ctx):
        key = self.name
        value = self.value.eval(ctx)
        ctx.var_def(key, value)


@dataclass
class If(Stmt):
    """
    Representa uma instrução condicional.

    Ex.: if (x > 0) { ... } else { ... }
    """

    cond: Expr
    then: Stmt
    orelse: Stmt

    def eval(self, ctx: Ctx):
        cond = self.cond.eval(ctx)
        if is_lox_true(cond):
            self.then.eval(ctx)
        else:
            self.orelse.eval(ctx)

    def emit_instructions(self):
        """
          start
            |
           B01--.
            |   |
        .--B02  |
        |       |
        |  B03<-/
        |   |
        \->end
        """
        orelse = Label()
        end = Label()

        # B01 (bloco da condição)
        yield from self.cond.emit_instructions()
        yield Instr("POP_JUMP_IF_FALSE", orelse)

        # B02 (bloco then)
        yield from emit_stmt_instructions(self.then)
        yield Instr("JUMP_ABSOLUTE", end)

        # B03 (bloco else)
        yield orelse
        yield from emit_stmt_instructions(self.orelse)

        # bloco end
        yield end



@dataclass
class While(Stmt):
    """
    Representa um laço de repetição.

    Ex.: while (x > 0) { ... }
    """

    cond: Expr
    body: Stmt

    def eval(self, ctx: Ctx):
        cond = self.cond.eval(ctx)
        if is_lox_true(cond):
            self.body.eval(ctx)
            self.eval(ctx)


    def emit_instructions(self):
        """
          start
            |
        .->B01--.
        |   |   |
        \--B02  |
                |
           end<-/
        """
        start = Label()
        end = Label()

        # B01 (bloco da condição)
        yield start
        yield from self.cond.emit_instructions()
        yield Instr("POP_JUMP_IF_FALSE", end)

        # B02 (bloco de comandos)
        yield from emit_stmt_instructions(self.body)
        yield Instr("JUMP_ABSOLUTE", start)

        # bloco end
        yield end


@dataclass
class Block(Stmt):
    """
    Representa bloco de comandos.

    Ex.: { var x = 42; print x;  }
    """

    stmts: list[Stmt]

    def eval(self, ctx: Ctx):
        ctx = ctx.push({})
        for stmt in self.stmts:
            stmt.eval(ctx)

    def emit_instructions(self):
        yield from emit_stmt_list(self.stmts)


@dataclass
class Function(Stmt):
    """
    Representa uma função.

    Ex.: fun f(x, y) { ... }
    """

    name: str
    arg_names: list[str]
    body: list[Stmt | Expr]

    def eval(self, ctx: Ctx):
        func = LoxFunction(self.arg_names, self.body, ctx)
        ctx.var_def(self.name, func)
        return func

    def to_function(self) -> FunctionType:
        """
        Converte função Lox para uma função Python correspondente
        """
        instructions = list(emit_stmt_list(self.body))
        if not instructions or not is_return_instr(instructions[-1]):
            instructions.append(Instr("LOAD_CONST", None))  # type: ignore
            instructions.append(Instr("RETURN_VALUE"))

        code = Bytecode(instructions)
        code.name = self.name
        code.argcount = len(self.arg_names)
        code.argnames = self.arg_names

        pycode = code.to_code()
        return FunctionType(pycode, {"print": ops.print}, self.name)


@dataclass
class Class(Stmt):
    """
    Representa uma classe.

    Ex.: class B < A { ... }
    """


def is_lox_true(value):
    return (value is not False) and (value is not None)


@dataclass
class LoxFunction:
    """
    Representa uma função lox em tempo de execução
    """

    arg_names: list[str]
    body: list[Stmt | Expr]
    ctx: Ctx

    def __call__(self, *values):
        """
        self.__call__(*args) <==> self(*args)
        """
        names = self.arg_names
        if len(names) != len(values):
            msg = f"esperava {len(names)} argumentos, recebeu {len(values)}"
            raise TypeError(msg)

        # Associa cada nome em names ao valor correspondente em values
        scope = dict(zip(names, values))

        # Avalia cada comando no corpo da função dentro do escopo local
        ctx = Ctx(scope, self.ctx)
        try:
            for stmt in self.body:
                stmt.eval(ctx)
        except LoxReturn as e:
            return e.value


class LoxReturn(Exception):
    value: Value

    def __init__(self, value):
        self.value = value
        super().__init__()


def is_return_instr(obj: Instr | Label) -> bool:
    if isinstance(obj, Label):
        return False
    return obj.name == "RETURN_VALUE"


def emit_stmt_list(stmts: list[Stmt | Expr]) -> Iterable[Instr | Label]:
    for stmt in stmts:
        yield from emit_stmt_instructions(stmt)


def emit_stmt_instructions(stmt: Stmt | Expr):
    yield from stmt.emit_instructions()
    if stmt.is_expr:
        yield Instr("POP_TOP")
