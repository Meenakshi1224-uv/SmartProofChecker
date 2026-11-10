from proof_engine import generate_proof, select_proof_method


def _build_ai_response(statement: str, method: str, steps):
    cleaned = " ".join((statement or "").split())
    if not cleaned:
        return "Please provide a valid mathematical statement so I can generate a proof."

    method_name = {
        "direct": "direct proof",
        "induction": "mathematical induction",
        "contradiction": "proof by contradiction",
        "contraposition": "proof by contraposition",
    }.get(method, method)

    step_text = " ".join(steps[:6]) if isinstance(steps, list) else str(steps)
    return (
        f"AI-generated reasoning for the statement '{cleaned}': "
        f"I analyze the claim using a {method_name}, begin with the required assumptions, "
        f"and structure the argument step by step. The key idea is to transform the statement into a clear logical chain, "
        f"validate the main condition, and conclude the result from the derived conditions. "
        f"Reasoning summary: {step_text}"
    )


def generate_ai_proof(statement: str, method: str = "direct"):
    requested_method = method
    selected_method = (
        select_proof_method(statement)
        if method.strip().lower() in {"auto", "ai", "ai generated", "automatic"}
        else method
    )
    if selected_method is None:
        return {
            "success": False,
            "method": "auto",
            "steps": [],
            "answer": None,
            "error": (
                "I couldn't match this statement to a supported proof pattern. "
                "Choose a method manually or try a supported example."
            ),
        }

    result = generate_proof(statement.strip() or "", selected_method)

    if isinstance(result, dict):
        steps = result.get("steps", [])
        answer = result.get("answer")
        method_name = result.get("method", selected_method)
        if result.get("success") is False:
            return result
        ai_response = _build_ai_response(statement, method_name, steps)
        return {
            "success": True,
            "requested_method": requested_method,
            "method": method_name,
            "steps": steps,
            "answer": answer,
            "ai_response": ai_response,
        }

    ai_response = _build_ai_response(statement, method, result)
    return {
        "success": True,
        "requested_method": requested_method,
        "method": selected_method,
        "steps": result,
        "answer": "Proof steps generated",
        "ai_response": ai_response,
    }
