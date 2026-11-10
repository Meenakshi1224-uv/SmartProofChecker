document.addEventListener("DOMContentLoaded", () => {
    const statementInput = document.getElementById("statement");
    const methodSelect = document.getElementById("proofMethod");
    const generateBtn = document.getElementById("generateBtn");
    const clearBtn = document.getElementById("clearBtn");
    const proofStatus = document.getElementById("proofStatus");
    const proofResult = document.getElementById("proofResult");
    const useGeneratedProofBtn = document.getElementById("useGeneratedProofBtn");
    const theoremInput = document.getElementById("theorem");
    const proofInput = document.getElementById("proof");
    const verifyBtn = document.getElementById("verifyBtn");
    const verificationResult = document.getElementById("verificationResult");
    let generatedSteps = [];

    const escapeHTML = (value) => String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");

    const displaySteps = (container, steps) => {
        if (!Array.isArray(steps)) {
            container.innerHTML = "<p>No steps returned.</p>";
            return;
        }
        container.innerHTML = `
            <h3>Solution Steps</h3>
            <ol>${steps.map((step) => `<li>${escapeHTML(step)}</li>`).join("")}</ol>
        `;
    };

    generateBtn.addEventListener("click", async () => {
        const statement = statementInput.value.trim();
        if (!statement) {
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
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ statement, method: methodSelect.value })
            });
            const data = await response.json();
            if (!response.ok || !data.success) {
                throw new Error(data.error || "Could not generate proof.");
            }
            proofStatus.textContent = "Proof generated successfully.";
            displaySteps(proofResult, data.steps);
            generatedSteps = Array.isArray(data.steps) ? data.steps : [];
            useGeneratedProofBtn.hidden = false;
            proofResult.innerHTML = `<h3>Selected Method</h3><p>${escapeHTML(data.method)}</p>` + proofResult.innerHTML;
            if (data.ai_response) {
                proofResult.innerHTML += `<h3>AI Generated Response</h3><p>${escapeHTML(data.ai_response)}</p>`;
            }
            if (data.answer !== null && data.answer !== undefined) {
                proofResult.innerHTML += `<h3>Answer</h3><p>${escapeHTML(JSON.stringify(data.answer))}</p>`;
            }
        } catch (error) {
            proofStatus.textContent = "Error generating proof.";
            proofResult.innerHTML = `<p>${escapeHTML(error.message)}</p>`;
            useGeneratedProofBtn.hidden = true;
        } finally {
            generateBtn.disabled = false;
            generateBtn.textContent = "Generate Proof";
        }
    });

    clearBtn.addEventListener("click", () => {
        statementInput.value = "";
        proofStatus.textContent = "";
        proofResult.innerHTML = "";
        generatedSteps = [];
        useGeneratedProofBtn.hidden = true;
    });

    useGeneratedProofBtn.addEventListener("click", () => {
        theoremInput.value = statementInput.value.trim();
        proofInput.value = generatedSteps.join("\n");
        document.getElementById("verification").scrollIntoView({ behavior: "smooth" });
        proofInput.focus();
    });

    verifyBtn.addEventListener("click", async () => {
        const statement = theoremInput.value.trim();
        const proof = proofInput.value.trim();
        if (!statement || !proof) {
            verificationResult.textContent = "Enter both the statement and proof.";
            return;
        }

        verifyBtn.disabled = true;
        verifyBtn.textContent = "Checking...";
        verificationResult.textContent = "";
        try {
            const response = await fetch("/api/verify-proof", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ statement, proof })
            });
            const data = await response.json();
            verificationResult.textContent = data.message || data.error || "Verification complete.";
        } catch (error) {
            verificationResult.textContent = `Error: ${error.message}`;
        } finally {
            verifyBtn.disabled = false;
            verifyBtn.textContent = "Verify Proof";
        }
    });
});
