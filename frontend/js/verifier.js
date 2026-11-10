document.addEventListener("DOMContentLoaded", () => {
    const theoremInput = document.getElementById("theorem");
    const proofInput = document.getElementById("proof");
    const verifyBtn = document.getElementById("verifyBtn");
    const verificationOutput = document.getElementById("verificationResult");

    const escapeHTML = (value) => String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");

    verifyBtn.addEventListener("click", async () => {
        const statement = theoremInput.value.trim();
        const proof = proofInput.value.trim();
        if (!statement || !proof) {
            verificationOutput.innerHTML = "<p>Please enter both the statement and the proof.</p>";
            return;
        }

        verifyBtn.disabled = true;
        verifyBtn.textContent = "Checking...";

        try {
            const response = await fetch("/api/verify-proof", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ statement, proof })
            });
            const data = await response.json();
            verificationOutput.innerHTML = `<p>${escapeHTML(data.message || data.error || "Verification complete.")}</p>`;
        } catch (error) {
            verificationOutput.innerHTML = `<p>Error: ${escapeHTML(error.message)}</p>`;
        } finally {
            verifyBtn.disabled = false;
            verifyBtn.textContent = "Verify Proof";
        }
    });
});
