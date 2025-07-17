# Linguagem Lox
Este é o código fonte para o interpretador de Lox que será desenvolvido ao 
longo do curso.

A única dependência externa é a biblioteca Lark. Use o método 
preferido de instalação do seu sistema para instalá-la. De modo geral, recomendo 
usar a ferramenta [uv](https://docs.astral.sh/uv/). Siga as instruções de 
instalação por lá e use o interpretador com o comando

    $ uv run lox
    
## Exercícios

Os exercícios são adicionados na pasta "exercícios" e podem ser arquivos Python
ou Markdown com as instruções de como proceder para resolução dos mesmos. 

Geralmente os arquivos Python devem ser editados e os arquivos Markdown descrevem
instruções sobre como modificar o código do módulo lox para cumprir o comando do
exercício.

A maior parte dos exercícios é testada automaticamente utilizando o Pytest. Neste
caso, existirá um arquivo correspondente na pasta tests com o nome `test_<nome do exercício>.py`. O Pytest detecta automaticamente estes arquivos e sabe o que 
fazer a partir daí.

## Rodando testes

Os testes automáticos podem ser executados com o comando

    $ uv run pytest

Se quiser maior controle, estude as opções que o pytest disponibiliza passando
a flag `--help`. O comando abaixo, por exemplo, mostra somente a primeira falha e
limita os testes ao módulo lex_numeros.

    $ uv run pytest --maxfail=1 -k lex_numeros