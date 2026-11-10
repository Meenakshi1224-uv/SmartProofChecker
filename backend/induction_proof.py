def generate_induction_proof(statement: str):
    text = (statement or "").strip().lower().replace(" ", "")
    if not text:
        return ["Please enter a mathematical statement."]

    if "1+2" in text and "n(n+1)/2" in text:
        return [
            "Step 1: Define P(n): 1 + 2 + ... + n = n(n+1)/2.",
            "Step 2: Check the base case: P(1) is true because 1 = 1(2)/2 = 1.",
            "Step 3: Assume P(k) is true for some integer k >= 1.",
            "Step 4: Then 1 + 2 + ... + k = k(k+1)/2.",
            "Step 5: Add (k+1) to both sides: 1 + 2 + ... + k + (k+1) = k(k+1)/2 + (k+1).",
            "Step 6: Simplify the right side: (k+1)(k+2)/2.",
            "Step 7: Therefore P(k+1) is true.",
            "Hence, by mathematical induction, the formula is true for all positive integers n."
        ]

    return [
        "Mathematical Induction",
        "Step 1: Identify the statement P(n).",
        "Step 2: Verify the base case P(1).",
        "Step 3: Assume P(k) is true.",
        "Step 4: Show P(k+1) is true.",
        "Step 5: Conclude the statement holds for all positive integers n.",
        "The exact induction proof for this statement is not implemented yet."
    ]
