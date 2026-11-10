
from flask import Flask, request, jsonify, send_from_directory, abort
import os
import sympy as sp

from database import add_history_entry, get_history, clear_history
from ai_proof_generator import generate_ai_proof
from proof_verifier import verify_proof

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app = Flask(__name__)


# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/dashboard")
def dashboard_page():
    return send_from_directory(FRONTEND_DIR, "dashboard.html")


# ---------------- STATIC FILES ----------------
@app.route("/css/<path:filename>")
def css_files(filename):
    return send_from_directory(os.path.join(FRONTEND_DIR, "css"), filename)


@app.route("/js/<path:filename>")
def js_files(filename):
    return send_from_directory(os.path.join(FRONTEND_DIR, "js"), filename)


@app.route("/assets/<path:filename>")
def asset_files(filename):
    return send_from_directory(os.path.join(FRONTEND_DIR, "assets"), filename)


@app.route("/<path:filename>")
def frontend_pages(filename):
    normalized = os.path.normpath(filename)
    if normalized.startswith(".."):
        abort(404)

    candidate = os.path.join(FRONTEND_DIR, normalized)
    if os.path.isfile(candidate):
        return send_from_directory(FRONTEND_DIR, normalized)

    html_candidate = os.path.join(FRONTEND_DIR, f"{normalized}.html")
    if os.path.isfile(html_candidate):
        return send_from_directory(FRONTEND_DIR, f"{normalized}.html")

    abort(404)


# ---------------- HEALTH CHECK ----------------
@app.route("/api/health")
def health():
    return jsonify({
        "success": True,
        "message": "SmartProofChecker is running"
    })


# ---------------- GENERATE PROOF ----------------
@app.route("/api/generate-proof", methods=["POST"])
def generate_proof_route():
    try:
        data = request.get_json(silent=True) or {}

        statement = data.get("statement", "").strip()
        method = data.get("method", "direct").strip().lower()

        if not statement:
            return jsonify({
                "success": False,
                "error": "Please enter a mathematical statement."
            }), 400

        result = generate_ai_proof(statement, method)
        if result.get("success") is False:
            return jsonify(result), 422

        if isinstance(result, dict):
            steps = result.get("steps", [])
            answer = result.get("answer")
            proof_method = result.get("method", method)
            ai_response = result.get("ai_response")
        else:
            steps = result
            answer = None
            proof_method = method
            ai_response = None

        result_entry = add_history_entry(statement, proof_method, answer, steps)

        return jsonify({
            "success": True,
            "requested_method": result.get("requested_method", method),
            "method": proof_method,
            "steps": steps,
            "answer": str(answer) if answer is not None else None,
            "ai_response": ai_response,
            "history_entry": result_entry
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ---------------- SOLVE ALGEBRA ----------------
@app.route("/api/solve-math", methods=["POST"])
def solve_math():
    try:
        data = request.get_json(silent=True) or {}
        expression = data.get("expression", "").strip()

        if not expression:
            return jsonify({
                "success": False,
                "error": "Please enter an equation."
            }), 400

        expression = expression.replace("^", "**")

        if "=" in expression:
            left, right = expression.split("=", 1)
            equation = sp.sympify(left) - sp.sympify(right)
            equation = sp.expand(equation)

            x = sp.Symbol("x")
            solutions = sp.solve(equation, x)

            steps = [
                f"Original equation: {left} = {right}",
                f"Move all terms to one side: {equation} = 0",
                f"Factorized form: {sp.factor(equation)} = 0",
                "Solve the equation:"
            ]

            for solution in solutions:
                steps.append(f"x = {solution}")

            return jsonify({
                "success": True,
                "steps": steps,
                "answer": [str(s) for s in solutions]
            })

        result = sp.sympify(expression)

        return jsonify({
            "success": True,
            "steps": [
                f"Original expression: {expression}",
                f"Simplified result: {sp.simplify(result)}",
                f"Expanded result: {sp.expand(result)}",
                f"Factorized result: {sp.factor(result)}"
            ],
            "answer": str(sp.simplify(result))
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400


# ---------------- VERIFY PROOF ----------------
@app.route("/api/verify-proof", methods=["POST"])
def verify_proof_route():
    try:
        data = request.get_json(silent=True) or {}

        statement = data.get("statement", "").strip()
        proof = data.get("proof", "").strip()

        if not statement or not proof:
            return jsonify({
                "success": False,
                "error": "Enter both statement and proof."
            }), 400

        result = verify_proof(statement, proof)
        return jsonify({
            "success": True,
            **result
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/history", methods=["GET"])
def history_route():
    return jsonify({
        "success": True,
        "history": get_history(20)
    })


@app.route("/api/history", methods=["DELETE"])
def clear_history_route():
    clear_history()
    return jsonify({
        "success": True,
        "message": "History cleared successfully."
    })


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(debug=True)
