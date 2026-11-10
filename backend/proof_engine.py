
import sympy as sp
import re


# =====================================================
# ALGEBRAIC EQUATION PROOF
# =====================================================

def algebraic_equation_proof(statement):

    try:
        statement = statement.replace("^", "**").strip()

        if "=" not in statement:
            return {
                "method": "Algebra",
                "steps": ["Please enter an equation using ="],
                "answer": None
            }

        lhs, rhs = statement.split("=", 1)

        x = sp.Symbol("x")

        left = sp.sympify(lhs)
        right = sp.sympify(rhs)

        equation = sp.expand(left - right)
        factored = sp.factor(equation)

        solutions = sp.solve(equation, x)

        steps = [
            f"Step 1: Original equation: {left} = {right}",
            f"Step 2: Move all terms to one side: {equation} = 0",
            f"Step 3: Factorize: {factored} = 0"
        ]

        if factored.is_Mul:
            steps.append(
                "Step 4: Apply the Zero Product Property."
            )
            steps.append(
                "Set each factor equal to zero."
            )

        steps.append("Final Step: Solve for x.")

        if solutions:
            for solution in solutions:
                steps.append(f"x = {solution}")
        else:
            steps.append("No solution found.")

        return {
            "method": "Algebraic Equation",
            "steps": steps,
            "answer": solutions
        }

    except Exception as e:
        return {
            "method": "Algebraic Equation",
            "steps": [f"Error: {str(e)}"],
            "answer": None
        }


# =====================================================
# DIRECT PROOF
# =====================================================

def direct_proof(statement):

    s = statement.lower()

    # Square of odd integer
    if "square" in s and "odd" in s:

        return [
            "Step 1: Let n be an odd integer.",
            "Step 2: n = 2k + 1, where k is an integer.",
            "Step 3: Square both sides.",
            "n² = (2k + 1)²",
            "Step 4: Expand.",
            "n² = 4k² + 4k + 1",
            "Step 5: Factor out 2.",
            "n² = 2(2k² + 2k) + 1",
            "Step 6: Since 2k² + 2k is an integer, n² is odd.",
            "Hence proved."
        ]

    # Sum of two odd numbers
    if "sum" in s and "odd" in s:

        return [
            "Step 1: Let a and b be odd integers.",
            "Step 2: a = 2m + 1 and b = 2n + 1.",
            "Step 3: Add them.",
            "a + b = 2m + 1 + 2n + 1",
            "Step 4: Simplify.",
            "a + b = 2(m + n + 1)",
            "Step 5: Therefore a + b is even.",
            "Hence proved."
        ]

    # Sum of two even numbers
    if "sum" in s and "even" in s:

        return [
            "Step 1: Let a and b be even integers.",
            "Step 2: a = 2m and b = 2n.",
            "Step 3: Add them.",
            "a + b = 2m + 2n",
            "Step 4: Factor out 2.",
            "a + b = 2(m + n)",
            "Step 5: Therefore a + b is even.",
            "Hence proved."
        ]

    return [
        "Direct Proof",
        "The statement is not recognized by the current proof rules.",
        "Please use a supported theorem or add a specific proof rule."
    ]


# =====================================================
# MATHEMATICAL INDUCTION
# =====================================================

def induction_proof(statement):

    s = statement.lower().replace(" ", "")

    # Sum of first n natural numbers
    if "1+2" in s and "n(n+1)/2" in s:

        return [
            "Step 1: Define P(n): 1 + 2 + ... + n = n(n+1)/2",
            "Step 2: Base Case n = 1.",
            "LHS = 1",
            "RHS = 1(1+1)/2 = 1",
            "Therefore P(1) is true.",
            "Step 3: Assume P(k) is true.",
            "1 + 2 + ... + k = k(k+1)/2",
            "Step 4: Prove P(k+1).",
            "1 + 2 + ... + k + (k+1)",
            "= k(k+1)/2 + (k+1)",
            "= (k+1)(k+2)/2",
            "Step 5: This is the required formula for k+1.",
            "Hence P(k+1) is true.",
            "Therefore the statement is true for all positive integers n."
        ]

    return [
        "Mathematical Induction",
        "Step 1: Identify the proposition P(n).",
        "Step 2: Verify the base case P(1).",
        "Step 3: Assume P(k) is true.",
        "Step 4: Use the assumption to prove P(k+1).",
        "Step 5: Conclude that P(n) holds for all positive integers n.",
        "The detailed derivation for this statement is not implemented."
    ]


# =====================================================
# PROOF BY CONTRADICTION
# =====================================================

def contradiction_proof(statement):

    s = statement.lower()

    if "sqrt" in s or "square root of 2" in s:

        return [
            "Step 1: Assume √2 is rational.",
            "Step 2: Then √2 = a/b, where a and b are coprime integers.",
            "Step 3: Square both sides.",
            "2 = a²/b²",
            "a² = 2b²",
            "Step 4: Therefore a² is even, so a is even.",
            "Let a = 2k.",
            "Step 5: Substitute.",
            "4k² = 2b²",
            "b² = 2k²",
            "Step 6: Therefore b is even.",
            "Step 7: Both a and b are even.",
            "This contradicts the assumption that a and b are coprime.",
            "Therefore √2 is irrational."
        ]

    return [
        "Proof by Contradiction",
        "Step 1: Assume the opposite of the statement.",
        "Step 2: Use mathematical definitions.",
        "Step 3: Derive a contradiction.",
        "Step 4: Reject the assumption.",
        "The detailed derivation for this statement is not implemented."
    ]


# =====================================================
# PROOF BY CONTRAPOSITION
# =====================================================

def contraposition_proof(statement):

    s = statement.lower()

    if "odd" in s and ("square" in s or "n^2" in s or "n²" in s):

        return [
            "Original statement: If n² is odd, then n is odd.",
            "Step 1: Prove the contrapositive.",
            "If n is even, then n² is even.",
            "Step 2: Let n = 2k.",
            "Step 3: Square both sides.",
            "n² = (2k)²",
            "n² = 4k²",
            "n² = 2(2k²)",
            "Step 4: Therefore n² is even.",
            "Step 5: The contrapositive is true.",
            "Hence the original statement is true."
        ]

    return [
        "Proof by Contraposition",
        "Step 1: Original statement is If P, then Q.",
        "Step 2: Contrapositive is If not Q, then not P.",
        "Step 3: Assume not Q.",
        "Step 4: Prove not P.",
        "Step 5: Conclude the original implication.",
        "The detailed derivation for this statement is not implemented."
    ]


def select_proof_method(statement):
    normalized = re.sub(r"\s+", "", statement.lower())
    normalized = normalized.replace("²", "^2").replace("√2", "sqrt(2)")

    if "1+2" in normalized and "n(n+1)/2" in normalized:
        return "induction"

    if "sqrt(2)" in normalized and "irrational" in normalized:
        return "contradiction"

    implication = normalized.split("then", 1)
    if (
        len(implication) == 2
        and "if" in implication[0]
        and "n^2" in implication[0]
        and "odd" in implication[0]
        and "n" in implication[1]
        and "odd" in implication[1]
    ):
        return "contraposition"

    if (
        "square" in normalized
        and "odd" in normalized
        and "even" not in normalized
        and "notodd" not in normalized
    ):
        return "direct"

    if "sum" in normalized and "twoodd" in normalized and "even" in normalized:
        return "direct"

    if "sum" in normalized and "twoeven" in normalized and "odd" not in normalized:
        return "direct"

    return None


# =====================================================
# MAIN PROOF GENERATOR
# =====================================================

def generate_proof(statement, method="direct"):

    statement = statement.strip()
    method = method.lower().strip()

    if not statement:
        return {
            "method": method,
            "steps": ["Please enter a statement."],
            "answer": None
        }

    if method in ["auto", "ai", "ai generated", "automatic"]:
        selected_method = select_proof_method(statement)
        if selected_method is None:
            return {
                "method": "auto",
                "steps": [],
                "answer": None,
                "success": False,
                "error": (
                    "I couldn't match this statement to a supported proof pattern. "
                    "Choose a method manually or try a supported example."
                )
            }
        method = selected_method

    if method in ["algebra", "algebraic", "equation"]:
        return algebraic_equation_proof(statement)

    if method in ["direct", "direct proof"]:
        steps = direct_proof(statement)

    elif method in ["induction", "mathematical induction"]:
        steps = induction_proof(statement)

    elif method in ["contradiction", "proof by contradiction"]:
        steps = contradiction_proof(statement)

    elif method in [
        "contraposition",
        "contrapositive",
        "proof by contraposition"
    ]:
        steps = contraposition_proof(statement)

    else:
        return {
            "method": method,
            "steps": ["Unknown proof method."],
            "answer": None
        }

    return {
        "method": method,
        "steps": steps,
        "answer": "Proof steps generated"
    }


# =====================================================
# COMPATIBILITY FUNCTIONS
# =====================================================

def generate_direct_proof(statement):
    return generate_proof(statement, "direct")


def generate_induction_proof(statement):
    return generate_proof(statement, "induction")


def generate_contradiction_proof(statement):
    return generate_proof(statement, "contradiction")


def generate_contraposition_proof(statement):
    return generate_proof(statement, "contraposition")
