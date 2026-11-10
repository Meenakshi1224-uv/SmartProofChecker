
document.addEventListener("DOMContentLoaded", function () {

    // =========================================
    // ELEMENTS
    // =========================================

    const statement = document.getElementById("statement");
    const proofMethod = document.getElementById("proofMethod");
    const generateBtn = document.getElementById("generateBtn");
    const clearBtn = document.getElementById("clearBtn");
    const proofResult = document.getElementById("proofResult");
    const proofStatus = document.getElementById("proofStatus");

    const mathInput = document.getElementById("mathInput");
    const solveMathBtn = document.getElementById("solveMathBtn");
    const clearMathBtn = document.getElementById("clearMathBtn");
    const mathResult = document.getElementById("mathResult");

    const verifyStatement = document.getElementById("verifyStatement");
    const verifyProof = document.getElementById("verifyProof");
    const verifyBtn = document.getElementById("verifyBtn");
    const verificationResult = document.getElementById("verificationResult");

    const themeToggle = document.getElementById("themeToggle");

    if (!generateBtn || !statement || !proofMethod || !proofResult || !proofStatus ||
        !solveMathBtn || !mathInput || !mathResult ||
        !verifyBtn || !verifyStatement || !verifyProof || !verificationResult) {
        if (themeToggle) {
            themeToggle.addEventListener("click", function () {
                document.body.classList.toggle("dark");
                themeToggle.textContent = document.body.classList.contains("dark") ? "☀️ Light Mode" : "🌙 Dark Mode";
            });
        }
        return;
    }


    // =========================================
    // SAFE HTML
    // =========================================

    function escapeHTML(text) {
        return String(text)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }


    // =========================================
    // DISPLAY STEPS
    // =========================================

    function displaySteps(container, steps) {

        if (!Array.isArray(steps)) {
            container.innerHTML = "<p>No steps returned.</p>";
            return;
        }

        container.innerHTML = `
            <h3>Solution Steps</h3>
            <ol>
                ${steps.map(step => `
                    <li>${escapeHTML(step)}</li>
                `).join("")}
            </ol>
        `;

        if (window.MathJax) {
            MathJax.typesetPromise([container]).catch(() => { });
        }
    }


    // =========================================
    // GENERATE PROOF
    // =========================================

    generateBtn.addEventListener("click", async function () {

        const text = statement.value.trim();
        const method = proofMethod.value;

        if (!text) {
            proofStatus.textContent = "Please enter a mathematical statement.";
            proofResult.innerHTML = "";
            return;
        }

        generateBtn.disabled = true;
        generateBtn.textContent = "Generating...";
        proofStatus.textContent = "Generating proof...";
        proofResult.innerHTML = "";

        try {

            const response = await fetch("/api/generate-proof", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    statement: text,
                    method: method
                })
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(data.error || "Proof generation failed.");
            }

            proofStatus.textContent = "Proof generated successfully.";

            displaySteps(proofResult, data.steps);

            if (data.ai_response) {
                proofResult.innerHTML += `
                    <h3>AI Generated Response</h3>
                    <p>${escapeHTML(data.ai_response)}</p>
                `;
            }

            if (data.answer !== null && data.answer !== undefined) {
                proofResult.innerHTML += `
                    <h3>Answer</h3>
                    <p>${escapeHTML(JSON.stringify(data.answer))}</p>
                `;
            }

        } catch (error) {

            proofStatus.textContent = "Error generating proof.";

            proofResult.innerHTML = `
                <p>${escapeHTML(error.message)}</p>
            `;

        } finally {

            generateBtn.disabled = false;
            generateBtn.textContent = "Generate Proof";
        }
    });


    // =========================================
    // CLEAR PROOF
    // =========================================

    clearBtn.addEventListener("click", function () {

        statement.value = "";
        proofResult.innerHTML = "";
        proofStatus.textContent = "";

    });


    // =========================================
    // ALGEBRA CALCULATOR
    // =========================================

    solveMathBtn.addEventListener("click", async function () {

        const expression = mathInput.value.trim();

        if (!expression) {
            mathResult.innerHTML = "<p>Please enter an equation.</p>";
            return;
        }

        solveMathBtn.disabled = true;
        solveMathBtn.textContent = "Solving...";
        mathResult.innerHTML = "";

        try {

            const response = await fetch("/api/solve-math", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    expression: expression
                })
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(data.error || "Unable to solve equation.");
            }

            displaySteps(mathResult, data.steps);

            mathResult.innerHTML += `
                <h3>Final Answer</h3>
                <p>${escapeHTML(JSON.stringify(data.answer))}</p>
            `;

        } catch (error) {

            mathResult.innerHTML = `
                <p>Error: ${escapeHTML(error.message)}</p>
            `;

        } finally {

            solveMathBtn.disabled = false;
            solveMathBtn.textContent = "Solve Equation";
        }
    });


    // =========================================
    // CLEAR ALGEBRA
    // =========================================

    clearMathBtn.addEventListener("click", function () {

        mathInput.value = "";
        mathResult.innerHTML = "";

    });


    // =========================================
    // VERIFY PROOF
    // =========================================

    verifyBtn.addEventListener("click", async function () {

        const theorem = verifyStatement.value.trim();
        const proof = verifyProof.value.trim();

        if (!theorem || !proof) {
            verificationResult.innerHTML =
                "<p>Please enter both statement and proof.</p>";
            return;
        }

        verifyBtn.disabled = true;
        verifyBtn.textContent = "Checking...";

        try {

            const response = await fetch("/api/verify-proof", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    statement: theorem,
                    proof: proof
                })
            });

            const data = await response.json();

            verificationResult.innerHTML = `
                <p>${escapeHTML(data.message || data.error)}</p>
            `;

        } catch (error) {

            verificationResult.innerHTML = `
                <p>Error: ${escapeHTML(error.message)}</p>
            `;

        } finally {

            verifyBtn.disabled = false;
            verifyBtn.textContent = "Verify Proof";
        }
    });


    // =========================================
    // DARK MODE
    // =========================================

    themeToggle.addEventListener("click", function () {

        document.body.classList.toggle("dark");

        if (document.body.classList.contains("dark")) {
            themeToggle.textContent = "☀️ Light Mode";
        } else {
            themeToggle.textContent = "🌙 Dark Mode";
        }

    });

});
