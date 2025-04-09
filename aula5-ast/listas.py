from lark import Lark, Transformer, Tree

grammar = r"""
?start   : list

list     : "["  "]"
         | "[" items "]"

?items   : item
         | item "," items
         
?item    : NUMBER
         | list

DIGIT    : "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
NUMBER   : DIGIT+

%ignore " " | "\n"
""" 

class ListTransformer(Transformer):
    def list(self, children):
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
    src = "[0,[42], 1,0]"
    
    print("src:", src)
    tree = parser.parse(src)
    tree_ = transformer.transform(tree)
    
    print("-" * 10)
    pprint(tree_)
