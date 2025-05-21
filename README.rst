=======
Avisos!
=======

* Link para entrega da prova: Turma 16-18h: https://classroom.github.com/a/mxz0caNP
* link2 https://classroom.github.com/a/rvOmLE7f



==============
Compiladores 1
==============

Este é o Git da disciplina Compiladores 1. Aqui ficará o material produzido em sala de aula 
assim como tarefas, wiki e discussões. Este arquivo contêm informações básicas sobre a disciplina e o 
plano de ensino do semestre.


Informações básicas
===================

Curso: 
    Engenharia de Software
Professor: 
    Fábio Macêdo Mendes
Disciplina: 
    Compiladores 1
Semestre/ano: 
    01/2025
Carga horária: 
    60 h
Créditos: 
    04


Ementa
======

* Introdução
* Autômatos
* Organização e estrutura de compiladores e interpretadores.
* Análise léxica.
* Expressões Regulares
* Análise sintática.
* Gramáticas Regulares e Livres de Contexto
* Estruturas de Dados e representação interna de código-fonte.
* Análise semântica.
* Geração de código.
* Máquinas abstratas e ambientes de tempo de execução.
* Projeto de Compiladores.
* Compiladores, Interpretadores e Parsers na Engenharia de Software.


Horário das aulas e atendimento
===============================

Aulas teóricas e de exercícios: quartas e sextas-feiras às 18h ou 20h.
Atendimento: realizado de forma assíncrona no grupo de Telegram da disciplina ou quartas-feiras às 10h no Lappis.


Informações importantes
========================

Este curso utiliza GitHub para gerenciar o curso. A comunicação com a 
turma é feita através de atualizações no Github ou no Microsoft Teams. 
Habilite a funcionalidade "Watch" no repositório para receber notificações sobre atualizações.

Cada aluno também deve preencher o formulário com nome, e-mail e usuário no Github.

* [Github](https://github.com/fcte-compiladores/2025-1/)
* [Github Classroom](https://classroom.github.com/a/8ynG-hQy)
* [Formulário de inscrição](https://docs.google.com/forms/d/12gy67ybJXSMaWfJ5ltfoFI0X4o8V9xGWXyoY89MhM6c/)


Critérios de avaliação
======================

A avaliação será feita com base em 4 tipos de atividades:

* 3 provas valendo 25% da nota, cada.
* Trabalho final valendo 25% da nota.
* Testes em sala de aula e listas de exercícios, valendo 25% da nota, no total.
* Desafios e atividades competitivas, valendo 5% da nota, como pontos extra.

Utilizamos as 4 melhores notas entre provas, trabalho final e testes.


Código de ética e conduta
-------------------------

Algumas avaliações serão realizadas com auxílio do computador. Todas as submissões 
serão processadas por um programa de detecção de plágio. Qualquer atividade onde for detectada a presença de 
plágio será anulada sem a possibilidade de substituição. Não será feita qualquer distinção entre o aluno que 
forneceu a resposta para cópia e o aluno que obteve a mesma.

As mesmas considerações também se aplicam às provas teóricas e atividades entregues no papel.


Prepare-se
==========

O curso utiliza alguns pacotes e ferramentas para os quais cada estudante deverá providenciar a instalação o mais 
cedo o possível. O curso requer Python 3.6+ com alguns pacotes instalados:

* Pip: Gerenciador de pacotes do Python (sudo apt-get install python3-pip)
* Jupyter notebook/nteract/Google colab: Ambiente de programação científica (https://nteract.io)
* Lark (pip3 install lark-parser --user): Biblioteca de parsing para Python. (note a **ausência** do sudo no comando!)
* Docker: cria ambientes completamente isolados para teste e validação (sudo apt-get install docker.io)

Já que vamos utilizar o Python, vale a pena instalar as seguintes ferramentas:

* [uv](https://docs.astral.sh/uv/): isola ambientes de desenvolvimento
* [ruff](https://docs.astral.sh/ruff/): busca erros de estilo e programação no seu código
* pytest, pytest-cov: criação de testes unitários
* hypothesis: auxilia na criação de testes unitários parametrizados.
  
DICA: em todos os casos, prefira instalar os pacotes Python utilizando o apt-get
ou o mecanismo que sua distribuição fornece e, somente se o pacote não existir, 
instale-o utilizando o pip. Se utilizar o pip, faça a instalação de usuário 
utilizando o comando ``pip3 install <pacote> --user`` (NUNCA utilize o sudo 
junto com --user e evite instalar globalmente para evitar problemas futuros com 
o APT). Melhor ainda: isole o ambiente utilizado em cada disciplina com uma 
ferramenta como o Virtualenv ou o Poetry_.

.. _Poetry: https://poetry.eustace.io


Linux e Docker
--------------

Os comandos de instalação acima assumem uma distribuição de Linux baseada em 
Debian. Não é necessário instalar uma distribuição deste tipo e você pode 
adaptar os comandos para o gerenciador de pacotes da sua distribuição (ou o 
Brew, no caso do OS X). Apesar do Linux não ser necessário para executar a maior 
parte das tarefas, é altamente recomendável que todos instalem o Docker para 
compartilharmos ambientes de desenvolvimento previsíveis (por exemplo, eu 
testarei as submissões em containers específicos que serão compartilhados com 
a turma). É possível executar o Docker em ambientes não-Linux utilizando o 
Docker Machine ou o Vagrant. Deste modo, cada aluno deve providenciar a 
instalação do Docker e Docker Compose na sua máquina.


Bibliografia principal
----------------------

* Crafting Interpreters, Robert Nystrom, 2015-2021. (https://craftinginterpreters.com/)
* **(SICP)** Structure and Interpretation of Computer Programs, Gerald Jay Sussman and Hal Abelson, MIT Press. (https://web.mit.edu/alexmv/6.037/sicp.pdf)


Material suplementar
--------------------

* **Curso de Python:** https://scrimba.com/learn/python
* **Curso de Python no Youtube (pt-BR):** https://www.youtube.com/watch?v=S9uPNppGsGo&list=PLvE-ZAFRgX8hnECDn1v9HNTI71veL3oW0


Cronograma de atividades
========================

Consultar `cronograma <CRONOGRAMA.rst>`_.

Obs.: O cronograma está sujeito a alterações.
