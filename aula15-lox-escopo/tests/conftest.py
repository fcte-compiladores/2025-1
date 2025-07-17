import re
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Callable, Iterable

import pytest

pytest.register_assert_rewrite("lox.testing")

from lox import testing  # noqa: E402

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


def pytest_addoption(parser):
    parser.addoption(
        "--full-suite",
        action="store_true",
        help="Run the full suite of tests. This includes all examples.",
    )


def pytest_runtest_setup(item):
    if "full_suite" in item.keywords and not item.config.getoption("--full-suite"):
        pytest.skip("need --full-suite option to run this test")


@pytest.fixture
def exercises_folder():
    """
    Retorna o caminho para a pasta de exercícios.
    """
    if EXERCISES.exists():
        return EXERCISES
    elif EXERCISES_ALT.exists():
        return EXERCISES_ALT
    else:
        raise FileNotFoundError(
            f"Não foi possível encontrar a pasta de exercícios. "
            f"Verifique se a pasta {EXERCISES} ou {EXERCISES_ALT} existe."
        )


@pytest.fixture()
def examples() -> Callable[[str], Iterable[testing.Example]]:
    """
    Carrega exemplos de código
    """

    return testing.load_examples


@pytest.fixture
def mod_loader(exercises_folder: Path):
    """
    Retorna o caminho para a pasta de exercícios.
    """

    def loader(name: str):
        file = exercises_folder / f"{name}.py"
        if not file.exists():
            raise FileNotFoundError(f"Arquivo {file} não encontrado.")

        ns: dict[str, Any] = {}
        with file.open("r") as fd:
            exec(fd.read(), ns)

        return SimpleNamespace(**ns)

    return loader
