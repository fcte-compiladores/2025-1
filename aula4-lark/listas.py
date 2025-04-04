# Use python3 -m pip install lark-parser
# para instalar o Lark
#
# O arquivo descreve uma linguagem que aceitas listas (potencialmente aninhadas)
# de elementos x. Aqui ilustramos um uso muito simples da biblioteca Lark.
# Veja mais em https://github.com/lark-parser/lark
import lark


grammar = r"""
start : list

list : "["  "]"
     | "[" elementos virgula "]"


elementos : dado
          | dado "," elementos
          
dado : "x"
     | list
     
virgula : "," 
        | epsilon
        
epsilon :
"""

parser = lark.Lark(grammar)
tree = parser.parse("[x,[x,]]")
print(tree.pretty())
