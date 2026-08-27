/* =================================
   PQ Assistant - Frontend Logic
   ================================= */

document.addEventListener("DOMContentLoaded", () => {

    const queryInput = document.getElementById("queryInput");
    const submitButton = document.getElementById("submitButton");
    const clearButton = document.getElementById("clearButton");

    const responseContent = document.getElementById("responseContent");
    const loadingMessage = document.getElementById("loadingMessage");
    const errorMessage = document.getElementById("errorMessage");

    /* ================================
       Submit Query
       ================================ */

    submitButton?.addEventListener("click", async () => {

        const query = queryInput.value.trim();

        if (!query) {
            showError("Please enter a query.");
            return;
        }

        hideError();
        showLoading();

        responseContent.textContent = "";

        try {

            const response = await fetch("/api/query", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    query: query
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.error || "Unable to process your query."
                );
            }

            displayResponse(data);

        } catch (error) {

            console.error("Query error:", error);

            showError(
                error.message || "Something went wrong. Please try again."
            );

        } finally {

            hideLoading();

        }
    });

    /* ================================
       Clear Query
       ================================ */

    clearButton?.addEventListener("click", () => {

        queryInput.value = "";
        responseContent.textContent = "";

        hideError();
        hideLoading();

        queryInput.focus();
    });

    /* ================================
       Enter Key Shortcut
       ================================ */

    queryInput?.addEventListener("keydown", (event) => {

        if (event.ctrlKey && event.key === "Enter") {
            submitButton.click();
        }

    });

    /* ================================
       Display Response
       ================================ */

    function displayResponse(data) {

        /*
         * Supports different response formats
         * from the Flask API.
         */

        const answer =
            data.answer ||
            data.response ||
            data.message ||
            "No response received.";

        responseContent.textContent = answer;
    }

    /* ================================
       Loading State
       ================================ */

    function showLoading() {

        if (loadingMessage) {
            loadingMessage.style.display = "block";
        }

        if (submitButton) {
            submitButton.disabled = true;
            submitButton.textContent = "Processing...";
        }
    }

    function hideLoading() {

        if (loadingMessage) {
            loadingMessage.style.display = "none";
        }

        if (submitButton) {
            submitButton.disabled = false;
            submitButton.textContent = "Ask PQ Assistant";
        }
    }

    /* ================================
       Error Handling
       ================================ */

    function showError(message) {

        if (!errorMessage) {
            return;
        }

        errorMessage.textContent = message;
        errorMessage.style.display = "block";
    }

    function hideError() {

        if (!errorMessage) {
            return;
        }

        errorMessage.textContent = "";
        errorMessage.style.display = "none";
    }

});