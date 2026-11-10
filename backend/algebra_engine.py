
import sympy as sp


x = sp.Symbol("x")


def solve_equation(equation):

    try:
        equation = equation.replace("^", "**").strip()

        if not equation:
            return {
                "success": False,
                "steps": ["Please enter an equation."]
            }

        if "=" not in equation:
            expression = sp.sympify(equation)

            return {
                "success": True,
                "steps": [
                    f"Original expression: {expression}",
                    f"Simplified: {sp.simplify(expression)}",
                    f"Expanded: {sp.expand(expression)}",
                    f"Factorized: {sp.factor(expression)}"
                ],
                "answer": str(sp.simplify(expression))
            }

        lhs, rhs = equation.split("=", 1)

        lhs = sp.sympify(lhs)
        rhs = sp.sympify(rhs)

        expression = sp.expand(lhs - rhs)
        factorized = sp.factor(expression)

        solutions = sp.solve(expression, x)

        steps = []

        steps.append(f"Step 1: Original equation: {lhs} = {rhs}")
        steps.append(f"Step 2: Move all terms to one side: {expression} = 0")
        steps.append(f"Step 3: Factorize: {factorized} = 0")

        if factorized.is_Mul:
            steps.append("Step 4: Apply the zero product property.")

        steps.append("Step 5: Solve for x.")

        for solution in solutions:
            steps.append(f"x = {solution}")

        return {
            "success": True,
            "steps": steps,
            "answer": [str(solution) for solution in solutions]
        }

    except Exception as e:

        return {
            "success": False,
            "steps": [f"Error: {str(e)}"]
        }


def simplify_expression(expression):

    try:
        expression = expression.replace("^", "**")

        result = sp.sympify(expression)

        return {
            "success": True,
            "original": str(result),
            "simplified": str(sp.simplify(result)),
            "expanded": str(sp.expand(result)),
            "factorized": str(sp.factor(result))
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }
