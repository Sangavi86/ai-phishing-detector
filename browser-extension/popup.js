document.addEventListener("DOMContentLoaded", () => {

    const scanBtn = document.getElementById("scanBtn");
    const resultDiv = document.getElementById("result");

    scanBtn.addEventListener("click", async () => {

        resultDiv.innerHTML = "<p>🔍 Scanning email...</p>";

        try {

            const tabs = await chrome.tabs.query({
                active: true,
                currentWindow: true
            });

            if (!tabs || tabs.length === 0) {
                resultDiv.innerHTML =
                    "<p style='color:red;'>No active tab found.</p>";
                return;
            }

            const tab = tabs[0];

            console.log("Current Tab:", tab);

            chrome.tabs.sendMessage(
                tab.id,
                { action: "getEmailText" },
                async (response) => {

                    if (chrome.runtime.lastError) {

                        console.error(
                            "Runtime Error:",
                            chrome.runtime.lastError.message
                        );

                        resultDiv.innerHTML = `
                            <div style="color:red;">
                                ❌ Content script not loaded.<br>
                                Refresh Gmail and try again.
                            </div>
                        `;
                        return;
                    }

                    console.log("EMAIL RESPONSE:", response);

                    if (!response || !response.text) {

                        resultDiv.innerHTML = `
                            <div style="color:red;">
                                ❌ No email content received.
                            </div>
                        `;
                        return;
                    }

                    const emailText = response.text;

                    console.log(
                        "EMAIL LENGTH:",
                        emailText.length
                    );

                    try {

                        const apiResponse = await fetch(
                            "http://127.0.0.1:5000/api/predict",
                            {
                                method: "POST",
                                headers: {
                                    "Content-Type": "application/json"
                                },
                                body: JSON.stringify({
                                    email: emailText
                                })
                            }
                        );

                        if (!apiResponse.ok) {

                            resultDiv.innerHTML = `
                                <div style="color:red;">
                                    ❌ Flask API Error
                                </div>
                            `;
                            return;
                        }

                        const data = await apiResponse.json();

                        console.log("API RESULT:", data);

                        const color =
                            data.risk === "High"
                                ? "#ff4d4f"
                                : "#22c55e";

                        resultDiv.innerHTML = `
                            <div style="
                                padding:15px;
                                border-radius:12px;
                                background:#f5f5f5;
                                margin-top:10px;
                            ">
                                <h2 style="
                                    color:${color};
                                    margin-bottom:10px;
                                ">
                                    ${data.result}
                                </h2>

                                <p>
                                    <strong>Risk:</strong>
                                    ${data.risk}
                                </p>

                                <p>
                                    <strong>Confidence:</strong>
                                    ${data.confidence}%
                                </p>

                                <p>
                                    <strong>Reasons:</strong>
                                </p>

                                <ul>
                                    ${
                                        data.reasons.length > 0
                                            ? data.reasons
                                                .map(
                                                    reason =>
                                                        `<li>${reason}</li>`
                                                )
                                                .join("")
                                            : "<li>No suspicious indicators found</li>"
                                    }
                                </ul>
                            </div>
                        `;

                    } catch (error) {

                        console.error(error);

                        resultDiv.innerHTML = `
                            <div style="color:red;">
                                ❌ Cannot connect to Flask server.
                                <br>
                                Make sure app.py is running.
                            </div>
                        `;
                    }
                }
            );

        } catch (error) {

            console.error(error);

            resultDiv.innerHTML = `
                <div style="color:red;">
                    ❌ Unexpected error occurred.
                </div>
            `;
        }
    });
});