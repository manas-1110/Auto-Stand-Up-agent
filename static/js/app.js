class StandUpApp {
    constructor() {
        this.init();
    }

    init() {
        this.bindEvents();
        this.checkSystemHealth();
        this.loadSavedValues();
    }

    bindEvents() {
        // Form submission
        document
            .getElementById("reportForm")
            .addEventListener("submit", (e) => {
                e.preventDefault();
                this.generateReport();
            });

        // Validation button
        document.getElementById("validateBtn").addEventListener("click", () => {
            this.validateRepository();
        });

        // Retry button
        document.getElementById("retryBtn").addEventListener("click", () => {
            this.hideError();
            this.generateReport();
        });

        // Copy button
        document.getElementById("copyBtn").addEventListener("click", () => {
            this.copyReport();
        });

        // Download button
        document.getElementById("downloadBtn").addEventListener("click", () => {
            this.downloadReport();
        });

        // Auto-save form values
        ["repoOwner", "repoName", "username", "days"].forEach((id) => {
            document.getElementById(id).addEventListener("input", (e) => {
                localStorage.setItem(`standupApp_${id}`, e.target.value);
            });
        });
    }

    loadSavedValues() {
        ["repoOwner", "repoName", "username", "days"].forEach((id) => {
            const saved = localStorage.getItem(`standupApp_${id}`);
            if (saved) {
                document.getElementById(id).value = saved;
            }
        });
    }

    async checkSystemHealth() {
        try {
            const response = await fetch("/api/health");
            const data = await response.json();

            const statusDot = document.getElementById("statusDot");
            const statusText = document.getElementById("statusText");

            if (
                data.status === "healthy" &&
                data.github_configured &&
                data.ai_configured
            ) {
                statusDot.classList.add("healthy");
                statusText.textContent = "System Ready";
            } else {
                statusDot.classList.add("unhealthy");
                let issues = [];
                if (!data.github_configured)
                    issues.push("GitHub not configured");
                if (!data.ai_configured) issues.push("AI not configured");
                statusText.textContent =
                    issues.length > 0 ? issues.join(", ") : "System Error";
            }
        } catch (error) {
            const statusDot = document.getElementById("statusDot");
            const statusText = document.getElementById("statusText");
            statusDot.classList.add("unhealthy");
            statusText.textContent = "Connection Error";
        }
    }

    async validateRepository() {
        const repoOwner = document.getElementById("repoOwner").value.trim();
        const repoName = document.getElementById("repoName").value.trim();

        if (!repoOwner || !repoName) {
            this.showError("Please enter both repository owner and name.");
            return;
        }

        const validateBtn = document.getElementById("validateBtn");
        const originalText = validateBtn.innerHTML;

        try {
            validateBtn.disabled = true;
            validateBtn.innerHTML =
                '<i class="fas fa-spinner fa-spin"></i> Validating...';

            const response = await fetch("/api/validate-repo", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    repo_owner: repoOwner,
                    repo_name: repoName,
                }),
            });

            const data = await response.json();

            if (data.success) {
                this.showRepositoryInfo(data.repo_info);
            } else {
                this.showError(`Repository validation failed: ${data.error}`);
            }
        } catch (error) {
            this.showError(`Error validating repository: ${error.message}`);
        } finally {
            validateBtn.disabled = false;
            validateBtn.innerHTML = originalText;
        }
    }

    showRepositoryInfo(repoInfo) {
        const repoInfoSection = document.getElementById("repoInfo");
        const repoInfoContent = document.getElementById("repoInfoContent");

        repoInfoContent.innerHTML = `
            <div class="repo-details">
                <h4>${repoInfo.full_name}</h4>
                ${
                    repoInfo.description
                        ? `<p class="repo-description">${repoInfo.description}</p>`
                        : ""
                }
                <div class="repo-info-grid">
                    <div class="repo-stat">
                        <div class="repo-stat-value">${
                            repoInfo.language || "N/A"
                        }</div>
                        <div class="repo-stat-label">Language</div>
                    </div>
                    <div class="repo-stat">
                        <div class="repo-stat-value">${repoInfo.stars.toLocaleString()}</div>
                        <div class="repo-stat-label">Stars</div>
                    </div>
                    <div class="repo-stat">
                        <div class="repo-stat-value">${repoInfo.forks.toLocaleString()}</div>
                        <div class="repo-stat-label">Forks</div>
                    </div>
                </div>
            </div>
        `;

        repoInfoSection.style.display = "block";
        repoInfoSection.scrollIntoView({ behavior: "smooth" });
    }

    async generateReport() {
        const formData = new FormData(document.getElementById("reportForm"));
        const data = Object.fromEntries(formData.entries());

        // Validate form
        if (
            !data.repo_owner ||
            !data.repo_name ||
            !data.username ||
            !data.days
        ) {
            this.showError("Please fill in all required fields.");
            return;
        }

        this.hideError();
        this.hideResults();
        this.showLoading();

        try {
            // Simulate progress steps
            this.updateProgressStep(1);

            const response = await fetch("/api/generate-report", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            });

            this.updateProgressStep(2);

            const result = await response.json();

            this.updateProgressStep(3);

            // Small delay to show the final step
            await new Promise((resolve) => setTimeout(resolve, 500));

            if (result.success) {
                this.showResults(result);
            } else {
                this.showError(result.error);
            }
        } catch (error) {
            this.showError(`Network error: ${error.message}`);
        } finally {
            this.hideLoading();
        }
    }

    showLoading() {
        document.getElementById("loadingSection").style.display = "block";
        document
            .getElementById("loadingSection")
            .scrollIntoView({ behavior: "smooth" });

        // Reset progress steps
        document.querySelectorAll(".step").forEach((step) => {
            step.classList.remove("active");
        });
    }

    hideLoading() {
        document.getElementById("loadingSection").style.display = "none";
    }

    updateProgressStep(stepNumber) {
        // Remove active from all steps
        document.querySelectorAll(".step").forEach((step) => {
            step.classList.remove("active");
        });

        // Add active to current and previous steps
        for (let i = 1; i <= stepNumber; i++) {
            const step = document.getElementById(`step${i}`);
            if (step) {
                step.classList.add("active");
            }
        }
    }

    showResults(result) {
        const resultsSection = document.getElementById("resultsSection");
        const reportMetadata = document.getElementById("reportMetadata");
        const reportContent = document.getElementById("reportContent");

        // Show metadata
        const metadata = result.metadata;
        const generatedDate = new Date(metadata.generated_at).toLocaleString();

        reportMetadata.innerHTML = `
            <div class="metadata-item">
                <div class="metadata-label">Repository</div>
                <div class="metadata-value">${metadata.repo_owner}/${
            metadata.repo_name
        }</div>
            </div>
            <div class="metadata-item">
                <div class="metadata-label">User</div>
                <div class="metadata-value">${metadata.username}</div>
            </div>
            <div class="metadata-item">
                <div class="metadata-label">Period</div>
                <div class="metadata-value">Last ${metadata.days} day${
            metadata.days > 1 ? "s" : ""
        }</div>
            </div>
            <div class="metadata-item">
                <div class="metadata-label">Generated</div>
                <div class="metadata-value">${generatedDate}</div>
            </div>
        `;

        // Show report content
        reportContent.textContent = result.report;

        // Store for export
        this.currentReport = result;

        resultsSection.style.display = "block";
        resultsSection.scrollIntoView({ behavior: "smooth" });
    }

    hideResults() {
        document.getElementById("resultsSection").style.display = "none";
    }

    showError(message) {
        const errorSection = document.getElementById("errorSection");
        const errorContent = document.getElementById("errorContent");

        errorContent.textContent = message;
        errorSection.style.display = "block";
        errorSection.scrollIntoView({ behavior: "smooth" });
    }

    hideError() {
        document.getElementById("errorSection").style.display = "none";
    }

    copyReport() {
        if (!this.currentReport) return;

        const reportText = this.formatReportForExport(this.currentReport);

        navigator.clipboard
            .writeText(reportText)
            .then(() => {
                const copyBtn = document.getElementById("copyBtn");
                const originalText = copyBtn.innerHTML;

                copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
                copyBtn.classList.add("btn-success");

                setTimeout(() => {
                    copyBtn.innerHTML = originalText;
                    copyBtn.classList.remove("btn-success");
                }, 2000);
            })
            .catch((err) => {
                this.showError("Failed to copy report to clipboard");
            });
    }

    downloadReport() {
        if (!this.currentReport) return;

        const reportText = this.formatReportForExport(this.currentReport);
        const blob = new Blob([reportText], { type: "text/plain" });
        const url = URL.createObjectURL(blob);

        const a = document.createElement("a");
        a.href = url;
        a.download = `standup-report-${this.currentReport.metadata.username}-${
            new Date().toISOString().split("T")[0]
        }.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    formatReportForExport(result) {
        const metadata = result.metadata;
        const generatedDate = new Date(metadata.generated_at).toLocaleString();

        return `STANDUP REPORT
================

Repository: ${metadata.repo_owner}/${metadata.repo_name}
User: ${metadata.username}
Analysis Period: Last ${metadata.days} day${metadata.days > 1 ? "s" : ""}
Generated: ${generatedDate}

REPORT:
-------
${result.report}

Generated by Auto Stand-Up Report Generator
`;
    }
}

// Initialize the app when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
    new StandUpApp();
});

// Add some utility functions for better UX
window.addEventListener("beforeunload", (e) => {
    // Warn user if they're in the middle of generating a report
    const loadingSection = document.getElementById("loadingSection");
    if (loadingSection && loadingSection.style.display === "block") {
        e.preventDefault();
        e.returnValue =
            "Report generation is in progress. Are you sure you want to leave?";
        return e.returnValue;
    }
});

// Add keyboard shortcuts
document.addEventListener("keydown", (e) => {
    // Ctrl/Cmd + Enter to generate report
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        e.preventDefault();
        const generateBtn = document.getElementById("generateBtn");
        if (generateBtn && !generateBtn.disabled) {
            generateBtn.click();
        }
    }

    // Escape to close error
    if (e.key === "Escape") {
        const errorSection = document.getElementById("errorSection");
        if (errorSection && errorSection.style.display === "block") {
            const app = window.standUpApp || new StandUpApp();
            app.hideError();
        }
    }
});
