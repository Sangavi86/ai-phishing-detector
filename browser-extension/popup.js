document.addEventListener("DOMContentLoaded", () => {

    const scanBtn = document.getElementById("scanBtn");
    const resultDiv = document.getElementById("result");

    scanBtn.addEventListener("click", async () => {

        resultDiv.innerHTML = "Scanning email...";

        try {

            const tabs = await chrome.tabs.query({
                active: true,
                currentWindow: true
            });

            const tab = tabs[0];

            chrome.tabs.sendMessage(
                tab.id,
                { action: "getEmailText" },
                async (response) => {

                    if (chrome.runtime.lastError) {

                        resultDiv.innerHTML = `
                            <div style="color:red">
                                Content script not loaded.<br>
                                Refresh Gmail and try again.
                            </div>
                        `;
                        return;
                    }

                    const emailText = response?.text || "";

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

                    const data = await apiResponse.json();

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
                                margin:0 0 10px 0;
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
                                    data.reasons
                                        .map(r => `<li>${r}</li>`)
                                        .join("")
                                }
                            </ul>
                        </div>
                    `;
                }
            );

        } catch (err) {

            console.error(err);

            resultDiv.innerHTML = `
                <div style="color:red">
                    Cannot connect to Flask server.
                </div>
            `;
        }
    });
});