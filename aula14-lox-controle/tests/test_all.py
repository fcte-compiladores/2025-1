import pytest
import lox.testing

EXAMPLES = [
    *lox.testing.load_examples(
        exclude={
            "benchmark",
            "scanning",
            "limit",
            "expressions",
            # Py-lox não impõe limites arbitrários
            "method/too_many_arguments",
            "method/too_many_parameters",
            "function/too_many_arguments",
            "function/too_many_parameters",
            # Py-lox não realiza o early binding
            "closure/close_over_method_parameter",
            "closure/assign_to_shadowed_later",
            "variable/early_bound",
            "function/local_mutual_recursion",
        }
    )
]


def get_id(example: lox.testing.Example):
    """
    Gera um ID para o exemplo.
    """
    prefix = str(lox.testing.EXAMPLES.absolute()) + "/"

    return str(example.path).removeprefix(prefix).removesuffix(".lox")


@pytest.mark.full_suite
@pytest.mark.parametrize("example", EXAMPLES, ids=map(get_id, EXAMPLES))
def test_all(example):
    example.run_checked()
