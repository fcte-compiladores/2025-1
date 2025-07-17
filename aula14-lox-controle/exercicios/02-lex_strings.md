[medio]

As strings do Lox funcionam de maneira um pouco diferente que outras linguagens
de programação.

Consulte https://craftinginterpreters.com/scanning.html#string-literals e
modifique a expressão regular em lox/grammar.lark para que ela corresponda ao 
formato especificado em lox.

Além disso, crie o método STRING em lox.LoxTransformer para processar os 
terminais de STRING corretamente:

    def STRING(self, token):
        data = process_strings()
        return Literal(data)

