import sympy as sp

X = sp.Symbol("x")


def normalize_expression(expression: str) -> str:
    if expression is None:
        return ""
    normalized = str(expression).strip()
    normalized = normalized.replace("^", "**")
    normalized = normalized.replace("?", "*").replace("?", "/")
    normalized = normalized.replace("?", "-").replace("?", "-")
    return normalized


def parse_equation(expression: str):
    cleaned = normalize_expression(expression)
    if not cleaned:
        raise ValueError("Please enter an equation.")
    if "=" not in cleaned:
        return None
    left, right = cleaned.split("=", 1)
    return sp.sympify(left), sp.sympify(right)


def solve_simple_equation(expression: str):
    parsed = parse_equation(expression)
    if parsed is None:
        raise ValueError("This is not an equation.")
    left, right = parsed
    equation = sp.expand(left - right)
    solutions = sp.solve(equation, X)
    return {
        "equation": str(equation),
        "solutions": [str(solution) for solution in solutions]
    }
