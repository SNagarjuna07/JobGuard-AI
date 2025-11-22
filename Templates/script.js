document.getElementById("jobForm").addEventListener("submit", predict);

async function predict(e) {
    e.preventDefault();

    const button = document.getElementById("btnSubmit");
    const loader = document.getElementById("loader");
    const result = document.getElementById("result-area");

    const title = document.getElementById("title").value.trim();
    const profile = document.getElementById("company_profile").value.trim();
    const description = document.getElementById("description").value.trim();
    const requirements = document.getElementById("requirements").value.trim();

    const combinedText = (title + profile + description + requirements).trim();
    if (combinedText.length === 0) return showResult("⚠ Enter job details.", true);

    button.disabled = true;
    loader.style.display = "block";
    result.innerHTML = "";

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

        const data = await response.json();
        console.log("DEBUG:", data);

        loader.style.display = "none";

        let realProb = Math.round(data.prob_real * 100);
        let fakeProb = Math.round(data.prob_fake * 100);

        let percent = 0;
        let probabilityText = "";
        let barColor = "";

        // FAKE JOB
        if (data.prediction === 1) {
            percent = fakeProb;
            probabilityText = `${percent}% Fake`;
            barColor = "fake";

            showResult(`
                <div class="status-card status-fake">
                    <h3>⚠ Fake Job Detected</h3>
                    <p>This posting shows scam-like patterns.</p>

                    <div class="prob-box">
                        <strong>Probability:</strong> ${probabilityText}
                        <div class="prob-bar ${barColor}" style="width:${percent}%"></div>
                    </div>
                </div>
            `);

        } else {
            // REAL JOB
            percent = 100 - fakeProb;
            probabilityText = `${percent}% Real`;
            barColor = "real";

            showResult(`
                <div class="status-card status-real">
                    <h3>✔ Likely Genuine Job</h3>
                    <p>This looks legitimate, but verify company contact details.</p>

                    <div class="prob-box">
                        <strong>Probability:</strong> ${probabilityText}
                        <div class="prob-bar ${barColor}" style="width:${percent}%"></div>
                    </div>
                </div>
            `);
        }

    } catch (error) {
        loader.style.display = "none";
        showResult("⚠ Server unreachable. Try again later.", true);
    }

    button.disabled = false;
}

function showResult(html, isError = false) {
    const result = document.getElementById("result-area");
    result.style.display = "block";
    result.innerHTML = html;
}
