# 1. implementar operadores matemáticos e comparações
# 2. implementar/testar expressões aninhadas
# 3. implementar/testar chamada de funções
# 4. implementar/testar leitura de atributos
# 5. operações unárias

import dis
import lox

def compile(src: str): 
    program = lox.parse(src)
    ast = program.stmts[0]
    assert isinstance(ast, lox.ast.Function)
    
    py_function = ast.to_function()
    
    print(f"LOX FUNCTION: {ast.name}")
    dis.dis(py_function)
    print()
    
    return py_function
    

src = """
fun func(n, i) {
    while (n > i) {
        print n;
    }
}
"""
    
func = compile(src)    

print(src)
print(f"{func(2, 1) = }")
