from lark import Lark, Transformer, Tree, v_args
from rich import print  # comente isso se quebrar, ou pip install rich

grammar = r"""
?start   : prog

?prog    : cmp
         | body ";" cmp

?body    : decl
         | body ";" decl
         
decl     : DEF "=" cmp

?cmp     : expr ">" expr   -> gt
         | expr "<" expr   -> lt
         | expr ">=" expr  -> ge
         | expr "<=" expr  -> le
         | expr "=" expr  -> eq
         | expr "=/=" expr  -> ne
         | expr

?expr    : expr "+" term  -> add
         | expr "-" term  -> sub
         | term

?term    : term ("*"|"×") pow   -> mul
         | term ("/"|"÷") pow   -> div 
         | pow

?pow     : atom ("^" | "🫠") pow
         | atom

?atom    : NUMBER 
         | VAR
         | "(" cmp ")"


VAR      : "x" | "y" | "z"
DEF      : "x" | "y" | "z"
NUMBER   : DIGIT+
DIGIT    : "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"

%ignore " " | "\n"
""" 

@v_args(inline=True)
class CalcTransformer(Transformer):  
    from operator import pow, add, sub, mul, truediv as div
    from operator import eq, ne, lt, le, gt, ge
    
    def __init__(self, visit_tokens = True):
        super().__init__(visit_tokens)
        self.env = {}
        
    def decl(self, name, value):
        self.env[name] = value
        
    def body(self, decl1, decl2):
        ...
    
    def prog(self, body, cmp):
        return cmp
    
    def NUMBER(self, token):
        return int(token)

    def DEF(self, token):
        return str(token)
    
    def VAR(self, token):
        name = str(token)
        return self.env[name]
    
    
transformer = CalcTransformer()
parser = Lark(grammar)

def pprint(obj):
    if hasattr(obj, "pretty"):
        print(obj.pretty())
    else:
        print(obj)


if __name__ == "__main__":
    src = "x = 2; y = x + 1; x * y"
    
    print("src:", src)
    tree = parser.parse(src)
    tree_ = transformer.transform(tree)
    print("-" * 10)
    pprint(tree_)
