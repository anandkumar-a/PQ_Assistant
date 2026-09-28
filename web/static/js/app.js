/* ============================================================
   PQ Assistant - Main Interactive Frontend Logic
   ============================================================ */

document.addEventListener("DOMContentLoaded", () => {

    /* ------------------------------------------------------------
       1. DOM Element References
       ------------------------------------------------------------ */
    // Core Query Elements
    const queryInput = document.getElementById("queryInput");
    const submitButton = document.getElementById("submitButton");
    const clearButton = document.getElementById("clearButton");
    const voiceInputBtn = document.getElementById("voiceInputBtn");
    const charCounter = document.getElementById("charCounter");
    const errorMessage = document.getElementById("errorMessage");
    const errorText = document.getElementById("errorText");

    // Settings & Advanced Controls
    const toggleAdvancedBtn = document.getElementById("toggleAdvancedBtn");
    const advancedOptionsPanel = document.getElementById("advancedOptionsPanel");
    const topKInput = document.getElementById("topKInput");
    const topKValue = document.getElementById("topKValue");
    const streamToggle = document.getElementById("streamToggle");
    const presetChips = document.querySelectorAll(".chip-btn");

    // Multi-Agent Pipeline Stepper
    const pipelineStepper = document.getElementById("pipelineStepper");
    const cancelStreamBtn = document.getElementById("cancelStreamBtn");
    const stepAgent1 = document.getElementById("step-agent1");
    const stepAgent2 = document.getElementById("step-agent2");
    const stepAgent3 = document.getElementById("step-agent3");
    const stepAgent4 = document.getElementById("step-agent4");

    // Response Section Elements
    const responseCard = document.getElementById("responseCard");
    const responseContent = document.getElementById("responseContent");
    const loadingMessage = document.getElementById("loadingMessage");
    const confidenceBadge = document.getElementById("confidenceBadge");
    const confidenceText = document.getElementById("confidenceText");
    const responseTimeBadge = document.getElementById("responseTimeBadge");
    const responseTimeText = document.getElementById("responseTimeText");
    const validationBadge = document.getElementById("validationBadge");
    const validationText = document.getElementById("validationText");

    // Action Buttons
    const copyAnswerBtn = document.getElementById("copyAnswerBtn");
    const ttsAnswerBtn = document.getElementById("ttsAnswerBtn");

    // Sources Accordion
    const sourcesContainer = document.getElementById("sourcesContainer");
    const toggleSourcesBtn = document.getElementById("toggleSourcesBtn");
    const sourcesList = document.getElementById("sourcesList");
    const sourceCountBadge = document.getElementById("sourceCountBadge");

    // Feedback Widget
    const feedbackSection = document.getElementById("feedbackSection");
    const starRating = document.getElementById("starRating");
    const feedbackCommentBox = document.getElementById("feedbackCommentBox");
    const feedbackCommentInput = document.getElementById("feedbackCommentInput");
    const submitFeedbackBtn = document.getElementById("submitFeedbackBtn");
    const feedbackThankYou = document.getElementById("feedbackThankYou");

    // Modals & Navigation Controls
    const themeToggleBtn = document.getElementById("themeToggleBtn");
    const healthStatusBtn = document.getElementById("healthStatusBtn");
    const healthStatusText = document.getElementById("healthStatusText");

    // Upload Modal
    const openUploadModalBtn = document.getElementById("openUploadModalBtn");
    const footerUploadLink = document.getElementById("footerUploadLink");
    const uploadModal = document.getElementById("uploadModal");
    const dropzone = document.getElementById("dropzone");
    const fileInput = document.getElementById("fileInput");
    const startUploadBtn = document.getElementById("startUploadBtn");
    const uploadFileName = document.getElementById("uploadFileName");
    const uploadFileSize = document.getElementById("uploadFileSize");
    const uploadProgressBar = document.getElementById("uploadProgressBar");
    const uploadProgressContainer = document.getElementById("uploadProgressContainer");
    const uploadStatusMessage = document.getElementById("uploadStatusMessage");

    // Analytics Modal
    const openAnalyticsModalBtn = document.getElementById("openAnalyticsModalBtn");
    const footerAnalyticsLink = document.getElementById("footerAnalyticsLink");
    const analyticsModal = document.getElementById("analyticsModal");
    const refreshAnalyticsBtn = document.getElementById("refreshAnalyticsBtn");
    const statTotalQueries = document.getElementById("statTotalQueries");
    const statAvgLatency = document.getElementById("statAvgLatency");
    const statValidationRate = document.getElementById("statValidationRate");

    // History Drawer
    const historyToggleBtn = document.getElementById("historyToggleBtn");
    const historyDrawer = document.getElementById("historyDrawer");
    const closeHistoryDrawerBtn = document.getElementById("closeHistoryDrawerBtn");
    const historySearchInput = document.getElementById("historySearchInput");
    const historyList = document.getElementById("historyList");
    const clearHistoryBtn = document.getElementById("clearHistoryBtn");

    const toastContainer = document.getElementById("toastContainer");

    /* ------------------------------------------------------------
       2. Application State Variables
       ------------------------------------------------------------ */
    let currentQueryId = null;
    let currentRating = 0;
    let activeAbortController = null;
    let selectedFileForUpload = null;
    let queryHistory = JSON.parse(localStorage.getItem("pq_query_history") || "[]");

    /* ------------------------------------------------------------
       3. Theme Initialization & Toggle
       ------------------------------------------------------------ */
    const savedTheme = localStorage.getItem("pq_theme") || "dark";
    document.documentElement.setAttribute("data-theme", savedTheme);

    themeToggleBtn?.addEventListener("click", () => {
        const currentTheme = document.documentElement.getAttribute("data-theme");
        const nextTheme = currentTheme === "dark" ? "light" : "dark";
        document.documentElement.setAttribute("data-theme", nextTheme);
        localStorage.setItem("pq_theme", nextTheme);
        showToast(`Switched to ${nextTheme} theme`, "info");
    });

    /* ------------------------------------------------------------
       4. Input Controls & Shortcuts
       ------------------------------------------------------------ */
    queryInput?.addEventListener("input", () => {
        const length = queryInput.value.length;
        charCounter.textContent = length;
        
        // Auto-expand textarea height up to 250px
        queryInput.style.height = "auto";
        queryInput.style.height = `${Math.min(queryInput.scrollHeight, 250)}px`;
    });

    queryInput?.addEventListener("keydown", (event) => {
        if (event.ctrlKey && event.key === "Enter") {
            event.preventDefault();
            submitButton.click();
        }
    });

    // Advanced Options Toggle
    toggleAdvancedBtn?.addEventListener("click", () => {
        advancedOptionsPanel.classList.toggle("hidden");
    });

    topKInput?.addEventListener("input", () => {
        topKValue.textContent = topKInput.value;
    });

    // Quick Preset Chips
    presetChips.forEach(chip => {
        chip.addEventListener("click", () => {
            const queryText = chip.getAttribute("data-query");
            if (queryText && queryInput) {
                queryInput.value = queryText;
                queryInput.dispatchEvent(new Event("input"));
                queryInput.focus();
                submitButton.click();
            }
        });
    });

    clearButton?.addEventListener("click", () => {
        queryInput.value = "";
        queryInput.dispatchEvent(new Event("input"));
        resetResponseUI();
        hideError();
        queryInput.focus();
    });

    /* ------------------------------------------------------------
       5. Voice Input Dictation
       ------------------------------------------------------------ */
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = null;

    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = "en-US";

        recognition.onstart = () => {
            voiceInputBtn.classList.add("btn-glow");
            voiceInputBtn.querySelector("span").textContent = "Listening...";
            showToast("Listening to voice input...", "info");
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            queryInput.value = (queryInput.value + " " + transcript).trim();
            queryInput.dispatchEvent(new Event("input"));
        };

        recognition.onend = () => {
            voiceInputBtn.classList.remove("btn-glow");
            voiceInputBtn.querySelector("span").textContent = "Voice";
        };

        recognition.onerror = (event) => {
            console.error("Speech recognition error:", event.error);
            showToast("Voice input failed or denied.", "error");
            recognition.stop();
        };

        voiceInputBtn?.addEventListener("click", () => {
            try {
                recognition.start();
            } catch (e) {
                recognition.stop();
            }
        });
    } else {
        if (voiceInputBtn) voiceInputBtn.style.display = "none";
    }

    /* ------------------------------------------------------------
       6. Primary Query Processing Logic
       ------------------------------------------------------------ */
    submitButton?.addEventListener("click", async () => {
        const query = queryInput.value.trim();

        if (!query) {
            showError("Please enter a query before submitting.");
            return;
        }

        hideError();
        resetResponseUI();
        showStepper();

        const topK = parseInt(topKInput.value, 10) || 5;
        const isStreaming = streamToggle ? streamToggle.checked : true;

        if (isStreaming) {
            await executeStreamingQuery(query, topK);
        } else {
            await executeStandardQuery(query, topK);
        }
    });

    cancelStreamBtn?.addEventListener("click", () => {
        if (activeAbortController) {
            activeAbortController.abort();
            activeAbortController = null;
            hideStepper();
            showToast("Query generation cancelled.", "info");
            submitButton.disabled = false;
        }
    });

    /* ------------------------------------------------------------
       7. Streaming Query Implementation (SSE)
       ------------------------------------------------------------ */
    async function executeStreamingQuery(query, topK) {
        activeAbortController = new AbortController();
        const signal = activeAbortController.signal;

        submitButton.disabled = true;
        updateStepperStage(1); // Agent 1
        
        let accumulatedAnswer = "";
        let startTime = performance.now();

        try {
            const response = await fetch("/query/stream", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: query, top_k: topK }),
                signal: signal
            });

            if (!response.ok) {
                const errData = await response.json().catch(() => ({}));
                throw new Error(errData.message || errData.error || `Server HTTP error: ${response.status}`);
            }

            // Prepare UI for token streaming
            responseContent.classList.remove("placeholder-mode");
            responseContent.innerHTML = "";

            const reader = response.body.getReader();
            const decoder = new TextDecoder("utf-8");
            let buffer = "";

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split("\n\n");
                buffer = lines.pop(); // keep trailing fragment

                for (const line of lines) {
                    const trimmed = line.trim();
                    if (!trimmed.startsWith("data: ")) continue;

                    const jsonStr = trimmed.replace(/^data:\s*/, "");
                    if (jsonStr === "[DONE]") {
                        updateStepperStage(4);
                        break;
                    }

                    try {
                        const event = JSON.parse(jsonStr);

                        if (event.type === "status") {
                            currentQueryId = event.query_id;
                            if (event.stage === "validated") {
                                updateStepperStage(2);
                                setTimeout(() => updateStepperStage(3), 300);
                            }
                        } else if (event.type === "token") {
                            updateStepperStage(3);
                            accumulatedAnswer += event.token;
                            renderFormattedMarkdown(responseContent, accumulatedAnswer);
                        } else if (event.type === "done") {
                            updateStepperStage(4);
                            currentQueryId = event.query_id;

                            const endTime = performance.now();
                            const elapsedSec = ((endTime - startTime) / 1000).toFixed(2);

                            displayMetadata({
                                confidence: event.confidence,
                                response_time: elapsedSec,
                                validated: event.validated,
                                sources: event.sources
                            });

                            saveToHistory(query, accumulatedAnswer, event.confidence);
                        } else if (event.type === "error") {
                            throw new Error(event.message || "Streaming error occurred.");
                        }
                    } catch (e) {
                        console.error("SSE parse error:", e, jsonStr);
                    }
                }
            }

        } catch (error) {
            if (error.name === "AbortError") return;
            console.error("Streaming error:", error);
            showError(error.message || "Failed to process streaming query.");
        } finally {
            hideStepper();
            submitButton.disabled = false;
            activeAbortController = null;
        }
    }

    /* ------------------------------------------------------------
       8. Standard Non-Streaming Query Implementation
       ------------------------------------------------------------ */
    async function executeStandardQuery(query, topK) {
        submitButton.disabled = true;
        
        // Progress stepper simulation
        updateStepperStage(1);
        const stageTimer = setInterval(() => {
            const currentActive = document.querySelector(".step-item.active");
            if (!currentActive) return;
            const currentId = currentActive.id;
            if (currentId === "step-agent1") updateStepperStage(2);
            else if (currentId === "step-agent2") updateStepperStage(3);
        }, 600);

        try {
            const response = await fetch("/query", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: query, top_k: topK })
            });

            clearInterval(stageTimer);

            const result = await response.json();

            if (!response.ok || !result.success) {
                const msg = result.error?.message || result.message || "Unable to process query.";
                throw new Error(msg);
            }

            updateStepperStage(4);

            const data = result.data || {};
            currentQueryId = data.query_id;

            responseContent.classList.remove("placeholder-mode");
            renderFormattedMarkdown(responseContent, data.answer || "No response generated.");

            displayMetadata({
                confidence: data.confidence,
                response_time: data.response_time,
                validated: data.validated,
                sources: data.sources || []
            });

            saveToHistory(query, data.answer, data.confidence);

        } catch (error) {
            clearInterval(stageTimer);
            console.error("Standard query error:", error);
            showError(error.message || "Unable to process query.");
        } finally {
            hideStepper();
            submitButton.disabled = false;
        }
    }

    /* ------------------------------------------------------------
       9. Formatting & Markdown Renderer
       ------------------------------------------------------------ */
    function renderFormattedMarkdown(container, text) {
        if (!text) return;

        if (window.marked && typeof window.marked.parse === "function") {
            container.innerHTML = window.marked.parse(text);
        } else {
            // Lightweight regex fallback for markdown
            let html = text
                .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
                .replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>')
                .replace(/`([^`]+)`/g, '<code>$1</code>')
                .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
                .replace(/\*([^*]+)\*/g, '<em>$1</em>')
                .replace(/\n\n/g, '</p><p>')
                .replace(/\n/g, '<br>');
            container.innerHTML = `<p>${html}</p>`;
        }
    }

    /* ------------------------------------------------------------
       10. UI Helpers & Metadata Display
       ------------------------------------------------------------ */
    function displayMetadata({ confidence, response_time, validated, sources }) {
        // Confidence
        if (confidence !== undefined && confidence !== null) {
            const pct = Math.round(confidence * 100);
            confidenceText.textContent = `Confidence: ${pct}%`;
            confidenceBadge.classList.remove("hidden");
        } else {
            confidenceText.textContent = "Confidence: Validated";
            confidenceBadge.classList.remove("hidden");
        }

        // Response Time
        if (response_time) {
            responseTimeText.textContent = `${response_time}s`;
            responseTimeBadge.classList.remove("hidden");
        }

        // Validation
        if (validated !== undefined) {
            validationText.textContent = validated ? "Verified Answer" : "Unverified / Suppressed";
            validationBadge.classList.remove("hidden");
        }

        // Sources
        if (sources && sources.length > 0) {
            sourceCountBadge.textContent = sources.length;
            renderSourcesList(sources);
            sourcesContainer.classList.remove("hidden");
        } else {
            sourcesContainer.classList.add("hidden");
        }

        // Feedback
        feedbackSection.classList.remove("hidden");
    }

    function renderSourcesList(sources) {
        sourcesList.innerHTML = "";
        sources.forEach((src, idx) => {
            const card = document.createElement("div");
            card.className = "source-item-card";

            const name = src.filename || src.source || src.title || `Source Doc #${idx + 1}`;
            const score = src.score ? `Match: ${Math.round(src.score * 100)}%` : `Rank #${idx + 1}`;
            const text = src.text || src.content || src.snippet || JSON.stringify(src);

            card.innerHTML = `
                <div class="source-item-header">
                    <span class="source-doc-name">📄 ${escapeHtml(name)}</span>
                    <span class="source-score">${escapeHtml(score)}</span>
                </div>
                <div class="source-snippet">${escapeHtml(text.substring(0, 240))}${text.length > 240 ? "..." : ""}</div>
            `;
            sourcesList.appendChild(card);
        });
    }

    toggleSourcesBtn?.addEventListener("click", () => {
        sourcesContainer.classList.toggle("open");
        sourcesList.classList.toggle("hidden");
    });

    /* ------------------------------------------------------------
       11. Action Buttons: Copy & Text-To-Speech
       ------------------------------------------------------------ */
    copyAnswerBtn?.addEventListener("click", async () => {
        const textToCopy = responseContent.innerText;
        if (!textToCopy) return;

        try {
            await navigator.clipboard.writeText(textToCopy);
            showToast("Copied answer to clipboard!", "success");
        } catch (e) {
            showToast("Failed to copy text.", "error");
        }
    });

    ttsAnswerBtn?.addEventListener("click", () => {
        const textToRead = responseContent.innerText;
        if (!textToRead || !window.speechSynthesis) return;

        if (window.speechSynthesis.speaking) {
            window.speechSynthesis.cancel();
            showToast("Audio stopped.", "info");
            return;
        }

        const utterance = new SpeechSynthesisUtterance(textToRead);
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        window.speechSynthesis.speak(utterance);
        showToast("Reading answer aloud...", "info");
    });

    /* ------------------------------------------------------------
       12. Star Rating & Feedback Submission
       ------------------------------------------------------------ */
    const stars = starRating?.querySelectorAll(".star");
    stars?.forEach((star) => {
        star.addEventListener("click", () => {
            currentRating = parseInt(star.getAttribute("data-value"), 10);
            updateStarDisplay(currentRating);
            feedbackCommentBox.classList.remove("hidden");
        });

        star.addEventListener("mouseover", () => {
            const val = parseInt(star.getAttribute("data-value"), 10);
            updateStarDisplay(val);
        });
    });

    starRating?.addEventListener("mouseleave", () => {
        updateStarDisplay(currentRating);
    });

    function updateStarDisplay(val) {
        stars?.forEach(s => {
            const sVal = parseInt(s.getAttribute("data-value"), 10);
            if (sVal <= val) s.classList.add("active");
            else s.classList.remove("active");
        });
    }

    submitFeedbackBtn?.addEventListener("click", async () => {
        if (!currentRating) {
            showToast("Please select a star rating.", "error");
            return;
        }

        try {
            const response = await fetch("/feedback", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    query_id: currentQueryId || "general",
                    rating: currentRating,
                    comments: feedbackCommentInput.value.trim()
                })
            });

            if (!response.ok) throw new Error("Failed to submit feedback.");

            feedbackCommentBox.classList.add("hidden");
            feedbackThankYou.classList.remove("hidden");
            showToast("Thank you for your feedback!", "success");

        } catch (e) {
            console.error("Feedback error:", e);
            showToast("Error recording feedback.", "error");
        }
    });

    /* ------------------------------------------------------------
       13. Document Upload Modal & Dropzone Handler
       ------------------------------------------------------------ */
    function openModal(modal) { modal?.classList.remove("hidden"); }
    function closeModal(modal) { modal?.classList.add("hidden"); }

    document.querySelectorAll("[data-close-modal]").forEach(btn => {
        btn.addEventListener("click", () => {
            const targetId = btn.getAttribute("data-close-modal");
            closeModal(document.getElementById(targetId));
        });
    });

    openUploadModalBtn?.addEventListener("click", () => openModal(uploadModal));
    footerUploadLink?.addEventListener("click", (e) => { e.preventDefault(); openModal(uploadModal); });

    dropzone?.addEventListener("click", () => fileInput.click());
    dropzone?.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropzone.classList.add("drag-over");
    });
    dropzone?.addEventListener("dragleave", () => dropzone.classList.remove("drag-over"));
    dropzone?.addEventListener("drop", (e) => {
        e.preventDefault();
        dropzone.classList.remove("drag-over");
        if (e.dataTransfer.files.length) handleFileSelection(e.dataTransfer.files[0]);
    });

    fileInput?.addEventListener("change", () => {
        if (fileInput.files.length) handleFileSelection(fileInput.files[0]);
    });

    function handleFileSelection(file) {
        selectedFileForUpload = file;
        uploadFileName.textContent = file.name;
        uploadFileSize.textContent = `${(file.size / 1024).toFixed(1)} KB`;
        uploadProgressContainer.classList.remove("hidden");
        startUploadBtn.disabled = false;
    }

    startUploadBtn?.addEventListener("click", async () => {
        if (!selectedFileForUpload) return;

        startUploadBtn.disabled = true;
        uploadProgressBar.style.width = "40%";
        uploadStatusMessage.classList.add("hidden");

        const formData = new FormData();
        formData.append("file", selectedFileForUpload);

        try {
            const response = await fetch("/upload", {
                method: "POST",
                body: formData
            });

            const res = await response.json();

            if (!response.ok || !res.success) {
                throw new Error(res.message || res.error || "Upload failed");
            }

            uploadProgressBar.style.width = "100%";
            showToast(`Document '${selectedFileForUpload.name}' uploaded!`, "success");
            setTimeout(() => {
                closeModal(uploadModal);
                resetUploadForm();
            }, 1000);

        } catch (e) {
            console.error("Upload error:", e);
            uploadProgressBar.style.width = "0%";
            uploadStatusMessage.textContent = e.message;
            uploadStatusMessage.classList.remove("hidden");
            showToast(e.message, "error");
        } finally {
            startUploadBtn.disabled = false;
        }
    });

    function resetUploadForm() {
        selectedFileForUpload = null;
        uploadProgressContainer.classList.add("hidden");
        uploadProgressBar.style.width = "0%";
        startUploadBtn.disabled = true;
        fileInput.value = "";
    }

    /* ------------------------------------------------------------
       14. Analytics Modal Handler
       ------------------------------------------------------------ */
    openAnalyticsModalBtn?.addEventListener("click", () => {
        openModal(analyticsModal);
        fetchAnalytics();
    });
    footerAnalyticsLink?.addEventListener("click", (e) => {
        e.preventDefault();
        openModal(analyticsModal);
        fetchAnalytics();
    });
    refreshAnalyticsBtn?.addEventListener("click", fetchAnalytics);

    async function fetchAnalytics() {
        try {
            const response = await fetch("/analytics");
            const res = await response.json();
            if (response.ok && res.success) {
                const d = res.data || {};
                statTotalQueries.textContent = d.total_queries || "0";
                statAvgLatency.textContent = `${d.average_response_time || 0.4}s`;
                statValidationRate.textContent = `${Math.round((d.validation_success_rate || 0.95) * 100)}%`;
            }
        } catch (e) {
            console.error("Analytics fetch failed:", e);
        }
    }

    /* ------------------------------------------------------------
       15. Health Check API Pill
       ------------------------------------------------------------ */
    healthStatusBtn?.addEventListener("click", checkHealth);

    async function checkHealth() {
        try {
            const response = await fetch("/health");
            const res = await response.json();
            if (response.ok && res.status === "healthy") {
                healthStatusText.textContent = "Pipeline Ready";
                healthStatusBtn.className = "status-pill green";
                showToast("System health check passed: Healthy", "success");
            } else {
                healthStatusText.textContent = "Service Degraded";
                healthStatusBtn.className = "status-pill yellow";
            }
        } catch (e) {
            healthStatusText.textContent = "Offline";
            healthStatusBtn.className = "status-pill red";
            showToast("Health check failed.", "error");
        }
    }

    /* ------------------------------------------------------------
       16. History Drawer Management
       ------------------------------------------------------------ */
    historyToggleBtn?.addEventListener("click", () => {
        renderHistoryList();
        historyDrawer.classList.remove("hidden");
    });

    closeHistoryDrawerBtn?.addEventListener("click", () => {
        historyDrawer.classList.add("hidden");
    });

    clearHistoryBtn?.addEventListener("click", () => {
        queryHistory = [];
        localStorage.removeItem("pq_query_history");
        renderHistoryList();
        showToast("Query history cleared.", "info");
    });

    historySearchInput?.addEventListener("input", () => {
        renderHistoryList(historySearchInput.value.trim().toLowerCase());
    });

    function saveToHistory(query, answer, confidence) {
        const item = {
            id: Date.now(),
            query: query,
            answer: answer,
            confidence: confidence,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };
        queryHistory.unshift(item);
        if (queryHistory.length > 30) queryHistory.pop();
        localStorage.setItem("pq_query_history", JSON.stringify(queryHistory));
    }

    function renderHistoryList(filter = "") {
        historyList.innerHTML = "";
        const filtered = queryHistory.filter(h => h.query.toLowerCase().includes(filter));

        if (filtered.length === 0) {
            historyList.innerHTML = `<div class="placeholder-empty"><small>No history found</small></div>`;
            return;
        }

        filtered.forEach(h => {
            const div = document.createElement("div");
            div.className = "history-item";
            div.innerHTML = `
                <div class="history-item-query">${escapeHtml(h.query)}</div>
                <div class="history-item-time">${h.timestamp} • ${h.confidence ? Math.round(h.confidence * 100) + "% confidence" : "Verified"}</div>
            `;
            div.addEventListener("click", () => {
                queryInput.value = h.query;
                queryInput.dispatchEvent(new Event("input"));
                responseContent.classList.remove("placeholder-mode");
                renderFormattedMarkdown(responseContent, h.answer);
                historyDrawer.classList.add("hidden");
                showToast("Loaded query from history.", "info");
            });
            historyList.appendChild(div);
        });
    }

    /* ------------------------------------------------------------
       17. Stepper & Error Helpers
       ------------------------------------------------------------ */
    function showStepper() {
        pipelineStepper.classList.remove("hidden");
        [stepAgent1, stepAgent2, stepAgent3, stepAgent4].forEach(s => s.className = "step-item");
    }

    function hideStepper() {
        pipelineStepper.classList.add("hidden");
    }

    function updateStepperStage(stageNumber) {
        const steps = [stepAgent1, stepAgent2, stepAgent3, stepAgent4];
        steps.forEach((step, idx) => {
            const num = idx + 1;
            if (num < stageNumber) {
                step.className = "step-item completed";
            } else if (num === stageNumber) {
                step.className = "step-item active";
            } else {
                step.className = "step-item";
            }
        });
    }

    function resetResponseUI() {
        responseContent.classList.add("placeholder-mode");
        responseContent.innerHTML = `
            <div class="placeholder-empty">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                </svg>
                <p>Your verified product answer will appear here in real-time.</p>
            </div>
        `;
        confidenceBadge.classList.add("hidden");
        responseTimeBadge.classList.add("hidden");
        validationBadge.classList.add("hidden");
        sourcesContainer.classList.add("hidden");
        feedbackSection.classList.add("hidden");
        feedbackThankYou.classList.add("hidden");
        feedbackCommentBox.classList.add("hidden");
        currentRating = 0;
        updateStarDisplay(0);
    }

    function showError(msg) {
        errorText.textContent = msg;
        errorMessage.classList.remove("hidden");
    }

    function hideError() {
        errorMessage.classList.add("hidden");
    }

    function showToast(message, type = "info") {
        if (!toastContainer) return;
        const toast = document.createElement("div");
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <span>${type === "success" ? "✓" : type === "error" ? "⚠️" : "ℹ️"}</span>
            <span>${escapeHtml(message)}</span>
        `;
        toastContainer.appendChild(toast);
        setTimeout(() => {
            toast.style.opacity = "0";
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    function escapeHtml(str) {
        return String(str)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

});