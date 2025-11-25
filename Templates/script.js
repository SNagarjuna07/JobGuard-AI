// Attach event listener to the form submission
document.getElementById("jobForm").addEventListener("submit", predict);

// Main prediction handler for JobGuard AI
async function predict(e) {
    e.preventDefault(); // Prevent default form submission

    // Get UI elements
    const button = document.getElementById("btnSubmit");
    const loader = document.getElementById("loader");
    const result = document.getElementById("result-area");

    // Retrieve user inputs
    const title = document.getElementById("title").value.trim();
    const profile = document.getElementById("company_profile").value.trim();
    const description = document.getElementById("description").value.trim();
    const requirements = document.getElementById("requirements").value.trim();

    // Combine all text fields for validation checks
    const combinedText = (title + " " + profile + " " + description + " " + requirements).trim();


    // Minimum Length Validation

    if (combinedText.split(" ").length < 10) {
        return showResult(`
            <div class="status-card status-fake">
                <h3>⚠ Not a Valid Job Posting</h3>
                <p>Please provide a valid job posting for accurate analysis.</p>
            </div>
        `, true);
    }


    // Gibberish / Nonsense Text Detection
    const gibberishPattern = /^[a-zA-Z]{1,4}$/;  

    if (gibberishPattern.test(title) || gibberishPattern.test(description)) {
        return showResult(`
            <div class="status-card status-fake">
                <h3>⚠ Invalid Job Posting</h3>
                <p>The text appears incomplete. Please provide a valid job posting.</p>
            </div>
        `, true);
    }

    // UI: Disable button and show loader during prediction
    button.disabled = true;
    loader.style.display = "block";
    result.innerHTML = "";

    // Send job details to Flask backend for ML inference
    try {
        const response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                title,
                company_profile: profile,
                description,
                requirements
            })
        });

        const data = await response.json();  // Parsed backend response
        loader.style.display = "none";       // Hide loader


        // Extract model probabilities
        let realProb = Math.round(data.prob_real * 100);
        let fakeProb = Math.round(data.prob_fake * 100);

        let percent = 0;
        let probabilityText = "";
        let barColor = "";

        // Prediction Handling: 1 = Fake Job, 0 = Real Job
        if (data.prediction === 1) {

            // Fake job detected
            percent = fakeProb;
            probabilityText = `${percent}% Fake`;
            barColor = "fake";

            showResult(`
                <div class="status-card status-fake">
                    <h3>⚠ Fake Job Detected</h3>
                    <p>This posting may be fraudulent or unsafe.</p>

                    <div class="prob-box">
                        <strong>Probability:</strong> ${probabilityText}
                        <div class="prob-bar ${barColor}" style="width:${percent}%"></div>
                    </div>
                </div>
            `);

        } else {

            // Real job detected
            percent = realProb;
            probabilityText = `${percent}% Real`;
            barColor = "real";

            showResult(`
                <div class="status-card status-real">
                    <h3>✔ Likely Genuine Job</h3>
                    <p>This job appears to be legitimate.</p>

                    <div class="prob-box">
                        <strong>Probability:</strong> ${probabilityText}
                        <div class="prob-bar ${barColor}" style="width:${percent}%"></div>
                    </div>
                </div>
            `);
        }

    } catch (error) {
        // Error handling: Backend unreachable or request failed
        loader.style.display = "none";
        showResult("⚠ Server unreachable. Please try again later.", true);
    }

    // Re-enable button after processing
    button.disabled = false;
}

// Utility function to display result HTML inside result box
function showResult(html, isError = false) {
    const result = document.getElementById("result-area");
    result.style.display = "block";
    result.innerHTML = html;
}