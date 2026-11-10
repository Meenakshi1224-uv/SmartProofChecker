def generate_contradiction_proof(statement: str):
    text = (statement or "").strip().lower()
    if not text:
        return ["Please enter a mathematical statement."]

    if "sqrt" in text or "square root of 2" in text or "sqrt2" in text:
        return [
            "Step 1: Assume, for contradiction, that \\sqrt{2} is rational.",
            "Step 2: Then \\sqrt{2} = a/b for integers a and b with gcd(a, b) = 1.",
            "Step 3: Squaring gives 2 = a^2 / b^2, so a^2 = 2b^2.",
            "Step 4: Therefore a is even; write a = 2k.",
            "Step 5: Substitute: 4k^2 = 2b^2, so b^2 = 2k^2.",
            "Step 6: Therefore b is also even.",
            "Step 7: This contradicts gcd(a, b) = 1.",
            "Hence, \\sqrt{2} is irrational."
        ]

    return [
        "Proof by Contradiction",
        "Step 1: Assume the opposite of the claim.",
        "Step 2: Derive a logical contradiction.",
        "Step 3: Conclude the original statement must be true.",
        "The exact contradiction proof for this statement is not implemented yet."
    ]
