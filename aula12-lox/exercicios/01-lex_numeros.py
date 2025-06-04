r"""
[facil]

A primeira versão do analisador léxico de Lox que implementamos usa a seguinte expressão
regular para identificar números:

    NUM: /([1-9][0-9]*|0)(\.[0-9]+)?/

Esta expressão é baseada no formato numérico do JSON e não do Lox! Dê uma olhada
no capítulo https://craftinginterpreters.com/scanning.html#number-literals e
escreva cinco exemplos de strings que representam números de cada categoria
abaixo, quando possível.

Se você não conseguir pensar em exemplos para uma categoria, escreva "nenhum" ou deixe uma lista vazia.
"""

VALIDOS_EM_AMBAS_ESPECIFICACOES: list[str] = [
    "1",
    "2.72",
    "3",
    "42",
    "5",
]

VALIDOS_EM_LOX_E_INVALIDOS_NA_NOSSA_VERSAO: list[str] = [
    "01",
    "02",
    "03.14",
    "04",
    "007",
]

VALIDOS_NA_NOSSA_VERSAO_E_INVALIDOS_EM_LOX: list[str] = []
