def generate_contraposition_proof(statement: str):
    text = (statement or "").strip().lower()
    if not text:
        return ["Please enter a mathematical statement."]

    if "odd" in text and "square" in text:
        return [
            "Original statement: If n^2 is odd, then n is odd.",
            "Step 1: Prove the contrapositive: If n is even, then n^2 is even.",
            "Step 2: Let n = 2k.",
            "Step 3: Square both sides: n^2 = (2k)^2 = 4k^2.",
            "Step 4: Factor: n^2 = 2(2k^2).",
            "Step 5: Since 2k^2 is an integer, n^2 is even.",
            "Therefore the contrapositive is true.",
            "Hence the original implication is true."
        ]

    return [
        "Proof by Contraposition",
        "Step 1: Write the original implication as If P, then Q.",
        "Step 2: Form the contrapositive: If not Q, then not P.",
        "Step 3: Assume not Q and prove not P.",
        "Step 4: Conclude the original implication is true.",
        "The exact contrapositive proof for this statement is not implemented yet."
    ]
