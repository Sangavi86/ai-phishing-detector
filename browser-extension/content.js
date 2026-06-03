console.log("CONTENT SCRIPT LOADED");

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {

    console.log("MESSAGE RECEIVED:", request);

    if (request.action === "getEmailText") {

        const emailText = document.body.innerText || "";

        console.log("EMAIL LENGTH:", emailText.length);

        sendResponse({
            text: emailText
        });

        return true;
    }
});