# 1. implementar operadores matemáticos
# 2. implementar/testar expressões aninhadas
# 3. implementar/testar chamada de funções
# 4. implementar/testar leitura de atributos

import dis
import lox
from bytecode import Bytecode, Instr
from typing import cast, Callable
from types import FunctionType

src = """
fun func(x, y) {
    return x + y;
}
"""

code = Bytecode([
    Instr("LOAD_FAST", "x"),
    Instr("LOAD_FAST", "y"),
    Instr("BINARY_ADD"),
    Instr("RETURN_VALUE"),
])
code.name = "func"
code.argnames = ["x", "y"]
code.argcount = 2
func = FunctionType(code.to_code(), {}, "func")

dis.dis(func)
print(f"{func(1, 2) = }")