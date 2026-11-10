# SmartProofChecker

A lightweight math proof assistant for algebra, direct proof generation, and proof verification.

The proof generator's **AI Generated (Choose a Method)** option selects among its built-in theorem patterns. Proof verification currently checks those same supported patterns; it is rule-based, not a general formal proof checker. Unsupported statements are reported as inconclusive.

## Run locally

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000 in the browser.
