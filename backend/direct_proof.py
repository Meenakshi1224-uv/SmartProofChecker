def generate_direct_proof(statement: str):
    text = (statement or "").strip()
    if not text:
        return ["Please enter a mathematical statement."]

    s = text.lower()

    if "square" in s and "odd" in s:
        return [
            "Step 1: Let n be an odd integer.",
            "Step 2: Write n = 2k + 1 for some integer k.",
            "Step 3: Square both sides: n^2 = (2k + 1)^2.",
            "Step 4: Expand: n^2 = 4k^2 + 4k + 1.",
            "Step 5: Rearrange as n^2 = 2(2k^2 + 2k) + 1.",
            "Step 6: Since 2k^2 + 2k is an integer, n^2 is odd.",
            "Hence, the square of an odd integer is odd."
        ]

    if "sum" in s and "odd" in s:
        return [
            "Step 1: Let a and b be odd integers.",
            "Step 2: Write a = 2m + 1 and b = 2n + 1.",
            "Step 3: Add the two numbers: a + b = 2m + 2n + 2.",
            "Step 4: Factor: a + b = 2(m + n + 1).",
            "Step 5: Since m + n + 1 is an integer, a + b is even.",
            "Hence, the sum of two odd integers is even."
        ]

    if "sum" in s and "even" in s:
        return [
            "Step 1: Let a and b be even integers.",
            "Step 2: Write a = 2m and b = 2n.",
            "Step 3: Add the two numbers: a + b = 2m + 2n.",
            "Step 4: Factor: a + b = 2(m + n).",
            "Step 5: Since m + n is an integer, a + b is even.",
            "Hence, the sum of two even integers is even."
        ]

    return [
        "Direct Proof",
        "The statement does not match a built-in direct proof pattern.",
        "Use a supported theorem or write a more specific statement."
    ]
