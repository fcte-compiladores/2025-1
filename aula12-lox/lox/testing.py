"""
ATENÇÃO: EVITE MODIFICAR ESTE ARQUIVO!

Funções que auxiliam na criação de testes e execução de exemplos.
"""

import contextlib
import io
import os
import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from lark import Tree, UnexpectedCharacters, UnexpectedToken

from . import Node, parse, eval as lox_eval
from .ctx import Ctx
from .errors import SemanticError

BASE_DIR = Path(__file__).parent.parent
EXERCISES = BASE_DIR / "exercicios"
EXAMPLES = BASE_DIR / "exemplos"
EXERCISES_ALT = BASE_DIR / "exercícios"
LEX_REGEX = re.compile(
    r"""
    (?://\ *expect:\ (?P<EXPECT>[^\n]*))
    | (?://\ *expect\ runtime\ error:\ (?P<RUNTIME_ERROR>[^\n]*))
    | (?://[^\n]*Error\ at\ '(?P<ERROR_AT>[^'\n]*)'[^\n]*)
    | (?://[^\n]*Error\ at\ end:(?P<ERROR_EOF>[^\n]*))
    | (?://[^\n]*Error:(?P<ERROR>[^\n]*))
    | (?P<COMMENT>//[^\n])
    | (?P<IGNORE>[^"/]+|"[^"]*"|//[^\n]*)
    """,
    re.VERBOSE,
)


@dataclass(frozen=True)
class Error:
    token: str | None = None
    line: int | None = None
    runtime: bool = False


@dataclass(frozen=True)
class Example:
    """
    Valores esperados dos exercícios.
    """

    src: str
    error: Error | None = None
    outputs: list[str] = field(default_factory=list)
    path: Path | None = None

    def __post_init__(self):
        for m in LEX_REGEX.finditer(self.src):
            if m.lastgroup == "IGNORE":
                continue
            elif m.lastgroup == "EXPECT":
                self.outputs.append(m.group("EXPECT"))
            elif m.lastgroup == "ERROR_AT":
                super().__setattr__("error", Error(token=m.group("ERROR_AT")))
                break
            elif m.lastgroup == "ERROR_EOF":
                super().__setattr__("error", Error(token=""))
                break
            elif m.lastgroup == "RUNTIME_ERROR":
                super().__setattr__("error", Error(token="", runtime=True))
                break
            elif m.lastgroup == "ERROR":
                super().__setattr__("error", Error())
                break

    @property
    def is_valid(self) -> bool:
        """
        Verifica se o exemplo possui uma sintaxe válida.
        """
        return self.error is None or self.error.runtime

    @property
    def expect_runtime_error(self) -> bool:
        """
        Verifica se o exemplo possui um erro de execução esperado.
        """
        return self.error is not None and self.error.runtime

    def run(self) -> tuple[Ctx, str]:
        """
        Executa o exemplo.
        """
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout) as stdout:
            ctx = Ctx()
            try:
                ctx = lox_eval(self.src, ctx)
            except Exception as e:
                if self.error is not None and self.error.runtime:
                    ctx["runtime-error"] = str(e)
                    return ctx, ""
                raise
        return ctx, stdout.getvalue()

    def run_checked(self):
        """
        Executa o exemplo e verifica a saída padrão e erros.
        """

        try:
            if self.is_valid:
                self.check_fully_converted()
                ctx, stdout = self.run()
                stdout = stdout.rstrip("\n")
                expect = "\n".join(self.outputs)
                if not self.expect_runtime_error:
                    assert expect == stdout
                else:
                    assert "runtime-error" in ctx
            else:
                try:
                    parse(self.src)
                except UnexpectedToken as e:
                    assert self.error.token == str(e.token) or self.error.token == str(
                        e.token_history[-1]
                    )
                except UnexpectedCharacters:
                    assert self.error.token is None
                except SemanticError as e:
                    assert self.error.token == str(e.token)
                else:
                    raise AssertionError(
                        "Esperava erro de sintaxe, mas isso não ocorreu."
                    )
        except:
            print("Erro ao executar o exemplo abaixo:")
            print(f"[{self.path.absolute()}]")
            print("\n    ".join(["", *self.src.splitlines(), ""]))
            print("Erros esperados:", self.error or "nenhum")
            raise

    def check_fully_converted(self):
        """
        Verifica se o exemplo foi totalmente convertido de CST para AST.
        """
        ast = parse(self.src)
        assert isinstance(ast, Node)

        def assert_not_lark(obj):
            if isinstance(obj, Tree):
                print(f"Esperava uma AST, mas encontrei um nó Lark do tipo {obj.data}:")
                print(obj.pretty())
                raise ValueError("árvore inválida")

        ast.visit({object: assert_not_lark})


def load_examples(name: str = "", exclude: set = set(), only: set | None = None):
    """
    Carrega exemplos de código.
    """
    visit = [EXAMPLES / name]
    if only is not None:
        filter = lambda name: normalize(name) in only  # noqa: E731
    elif not exclude:
        filter = lambda _: True  # noqa: E731
    else:
        filter = lambda name: normalize(name) not in exclude  # noqa: E731

    while visit:
        path = visit.pop()
        if not path.exists():
            raise FileNotFoundError(f"Arquivo {path} não encontrado.")

        for child in path.iterdir():
            if child.is_dir():
                if filter(child):
                    visit.append(child)
            elif filter(child) and child.suffix == ".lox":
                yield load_example(child)


@lru_cache(maxsize=512)
def load_example(place: Path) -> Example:
    return Example(place.read_text(encoding="utf-8"), path=place)


@lru_cache(maxsize=512)
def normalize(name: Path) -> str:
    """
    Normaliza o nome do arquivo.
    """
    return str(name).removeprefix(str(EXAMPLES) + os.path.sep).removesuffix(".lox")
