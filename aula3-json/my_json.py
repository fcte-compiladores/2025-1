from typing import Any


def read_json(src: str) -> Any:
    chars = list(reversed(src))
    return read_value(chars)


def read_value(chars: list[str]):
    ws(chars)
    match chars[-1]:
        case "t":
            value = read_literal("true", chars, True)
        case "f":
            value = read_literal("false", chars, False)
        case "n":
            value = read_literal("null", chars, None)
        case "{":
            value = read_object(chars)
        case "[":
            value = read_array(chars)
        case '"':
            value = read_string(chars)
        case '-':
            chars.pop()
            value = -read_number(chars)
        case c if c.isdigit():
            value = read_number(chars)
        case _:
            raise SyntaxError 
    ws(chars)
    return value

    
def ws(chars: list[str]):
    while chars and chars[-1] in " \n\t\r":
        chars.pop()


def read_literal(lit: str, chars: list[str], value):
    for c in lit:
        if c != chars.pop():
            raise SyntaxError
    return value


def read_number(chars: list[str]) -> int:
    if chars[-1] == "0":
        chars.pop()
        return 0
    
    ns = []
    while chars and chars[-1] in "0123456789":
        n = chars.pop()
        ns.append(n)
    return int("".join(ns))


def read_string(chars: list[str]) -> str:
    if chars.pop() != '"':
        raise SyntaxError
    parts = []
    while (c := chars.pop()) != '"':
        parts.append(c)
    return "".join(parts)


def read_array(chars: list[str]) -> list:
    if chars.pop() != "[":
        raise SyntaxError
    ws(chars)
    
    if chars[-1] == "]":
        chars.pop()
        return []

    values = []
    while True:
        value = read_value(chars)
        values.append(value)
        
        c = chars.pop()
        if c == ",":
            continue
        elif c == "]":
            break
        else:
            raise SyntaxError
    
    return values


if __name__ == "__main__":
    import json 
    import time

    print(read_json("null"))
    print(read_json("42") + 1)
    print(read_json('"Fabio"'))
    print(read_json('[1, "Fabio", [1, 2, [[]]], "compiladores"]'))

    src = '[1, "Fabio", [1, 2, [[]]], "compiladores"]'
    
    t0 = time.time()
    for _ in range(1000):
        json.loads(src)
    print("json.loads:", time.time() - t0)

    t0 = time.time()
    for _ in range(1000):
        read_json(src)
    print("read_json:", time.time() - t0)