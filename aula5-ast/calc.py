from lark import Lark, Transformer, Tree

grammar = r"""
?start   : list 

list     : "["  "]"
         | "[" items "]"

items    : item            -> single
         | item "," items
         
?item    : math
         | list
         
?math    : atom OP math  
         | atom
         
?atom    : NUMBER
         | list

OP       : "+" | "*" | "-" | "/" | "**"

DIGIT    : "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
NUMBER   : DIGIT+

%ignore " " | "\n"
""" 

class ListTransformer(Transformer):
    def list(self, children):
        return children[0]
    
    def math(self, children):
        x, op, y  = children
        return  eval(f"{x} {op} {y}")
    
    def single(self, children):
        return children
    
    def items(self, children):
        head, tail = children
        if isinstance(children[1], list):
            return [head, *tail]
        return children
    
    def NUMBER(self, token):
        return int(token)

transformer = ListTransformer()
parser = Lark(grammar)

def pprint(obj):
    if hasattr(obj, "pretty"):
        print(obj.pretty())
    else:
        print(obj)


if __name__ == "__main__":
    src = "[[1] + [2, 3]]"
    
    print("src:", src)
    tree = parser.parse(src)
    tree_ = transformer.transform(tree)
    
    print("-" * 10)
    pprint(tree_)
