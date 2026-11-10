
import sympy as sp
import re


def _normalize(text):
    normalized = text.lower().replace("²", "^2").replace("√2", "sqrt(2)")
    return re.sub(r"[\s.,;:]", "", normalized)


def _required_proof_parts(statement):
    normalized = _normalize(statement)

    if "1+2" in normalized and "n(n+1)/2" in normalized:
        return "induction", (
            "basecase",
            "assumep(k)",
            "k(k+1)/2",
            "(k+1)(k+2)/2",
            "hencep(k+1)istrue",
        )

    if "sqrt(2)" in normalized and "irrational" in normalized:
        return "contradiction", (
            "sqrt(2)isrational",
            "coprime",
            "a^2=2b^2",
            "a=2k",
            "b^2=2k^2",
            "contradict",
            "irrational",
        )

    implication = normalized.split("then", 1)
    if (
        len(implication) == 2
        and "if" in implication[0]
        and "n^2" in implication[0]
        and "odd" in implication[0]
        and "n" in implication[1]
        and "odd" in implication[1]
    ):
        return "contraposition", (
            "contrapositive",
            "n=2k",
            "n^2=2(2k^2)",
            "even",
            "originalstatementistrue",
        )

    if (
        "square" in normalized
        and "odd" in normalized
        and "even" not in normalized
        and "notodd" not in normalized
    ):
        return "direct", (
            "n=2k+1",
            "n^2=2(2k^2+2k)+1",
            "integer",
            "odd",
            "henceproved",
        )

    if "sum" in normalized and "twoodd" in normalized and "even" in normalized:
        return "direct", (
            "a=2m+1",
            "b=2n+1",
            "a+b=2(m+n+1)",
            "even",
            "henceproved",
        )

    if "sum" in normalized and "twoeven" in normalized and "odd" not in normalized:
        return "direct", (
            "a=2m",
            "b=2n",
            "a+b=2(m+n)",
            "even",
            "henceproved",
        )

    return None


def verify_proof(statement, proof):

    statement = statement.strip()
    proof = proof.strip()

    if not statement:
        return {
            "verified": False,
            "message": "Please enter a mathematical statement."
        }

    if not proof:
        return {
            "verified": False,
            "message": "Please enter your proof."
        }

    supported_proof = _required_proof_parts(statement)
    if supported_proof is None:
        return {
            "verified": False,
            "status": "unsupported",
            "message": (
                "This statement is outside the verifier's supported theorem patterns, "
                "so the proof could not be verified automatically."
            )
        }

    method, required_parts = supported_proof
    normalized_proof = _normalize(proof)
    missing_parts = [part for part in required_parts if part not in normalized_proof]
    if missing_parts:
        return {
            "verified": False,
            "status": "incomplete",
            "method": method,
            "message": (
                "The proof is incomplete for the recognized theorem. "
                "Include the key definitions, derivation, and conclusion for this proof method."
            )
        }

    return {
        "verified": True,
        "status": "verified",
        "method": method,
        "message": (
            f"The proof matches the supported {method} proof pattern. "
            "This is a rule-based check, not a general formal proof checker."
        )
    }


def verify_equation(equation):

    try:
        equation = equation.replace("^", "**")

        if "=" not in equation:
            return {
                "verified": False,
                "message": "Invalid equation."
            }

        lhs, rhs = equation.split("=", 1)

        result = sp.simplify(
            sp.sympify(lhs) - sp.sympify(rhs)
        )

        return {
            "verified": result == 0,
            "message": (
                "Equation is an identity."
                if result == 0
                else "Equation is not an identity."
            )
        }

    except Exception as e:
        return {
            "verified": False,
            "message": str(e)
        }
