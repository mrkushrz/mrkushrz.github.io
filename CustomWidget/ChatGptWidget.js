(function () {
    let template = document.createElement("template");
    template.innerHTML = `
    <style>
    .main-container {
        display: flex; /* Use flexbox layout */
        flex-wrap: wrap; /* Allow items to wrap */
    }

    .image-container {
        /* Adjust the image-container size if needed */
        display: flex;
        align-items: center; /* Center the image vertically */
        justify-content: center; /* Center the image horizontally */
    }

    .input-fields-container {
        display: flex;
        flex-direction: column; /* Stack the input containers vertically */
    }

    .input-container {
        justify-content: space-between;
        align-items: center;
        display: flex;
        margin-bottom: 10px;
    }

    .input-container > label {
        margin-right: 10px; /* 10px space between label and input */
    }

    .input-container > input[type="date"], .input-container > button {
        padding: 10px;
        font-size: 16px;
        border: 1px solid #ccc;
        border-radius: 50px;
    }

    .input-container > input[type="date"] {
        margin-right: 10px; /* 10px space between input and button */
    }

    .input-container > button {
        margin-left: auto;
        background-color: #3cb6a9;
        color: #fff;
        border: none;
        cursor: pointer;
    }

    .input-container > button:active {
        background-color: #2a8076; /* Darker shade for active state */
    }

    .output-container, .reset-button-container {
        width: 100%; /* Take up the full width available */
    }

    textarea {
        padding: 10px;
        font-size: 16px;
        border: 1px solid #ccc;
        border-radius: 5px;
        width: 100%;
        max-width: 620px;
    }

    button {
        padding: 10px;
        font-size: 16px;
        background-color: #3cb6a9;
        color: #fff;
        border: none;
        border-radius: 50px;
        cursor: pointer;
    }

    button:active {
        background-color: #2a8076; /* Darker shade of the original green for active state */
    }

</style>

<div class="main-container">
    <div class="image-container">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/ChatGPT-Logo.png/1200px-ChatGPT-Logo.png" alt="ChatGPT Logo" style="width: 150px;"/>
    </div>
    
    <div class="input-fields-container">
        <!-- Analysis Container -->
        <div class="input-container" id="analysis-container">
            <label for="start-date">Start</label>
            <input type="date" id="start-date">
            <label for="end-date">End</label>
            <input type="date" id="end-date">
            <button id="analysis-button">Analysis</button>
        </div>

        <!-- Forecast Container -->
        <div class="input-container" id="forecast-container">
            <label for="forecast-date">Forecast End</label>
            <input type="date" id="forecast-date">
            <button id="forecast-button">Forecast</button>
        </div>
    </div>

    <div class="output-container">
        <textarea id="generated-text" rows="10" readonly></textarea>
    </div>

    <div class="reset-button-container">
        <button id="reset-button">Reset</button>
    </div>
</div>
    `;

    class Widget extends HTMLElement {
        constructor() {
            super();
            let shadowRoot = this.attachShadow({mode: "open"});
            shadowRoot.appendChild(template.content.cloneNode(true));
            this._props = {};
            this.commodity = "europeansugar";
        }

        async connectedCallback() {
            this.init();
        }

        async updateCommodity(selection){
            return this.commodity = selection;
        }

        async init() {
            const analysisButton = this.shadowRoot.getElementById("analysis-button");
            analysisButton.addEventListener("click", async () => {
                const startDate = this.convertDate(this.shadowRoot.getElementById("start-date").value);
                const endDate = this.convertDate(this.shadowRoot.getElementById("end-date").value);
                const generatedText = this.shadowRoot.getElementById("generated-text");
                generatedText.value = "Analysis in progress...";
                // Implement the analysis logic and fetch call here
                try {
                    const response = await fetch("https://finaigpt-public.eu.ngrok.io/generate_response", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            // Add any additional headers your backend requires
                        },
                        body: JSON.stringify({
                            start_date: startDate,
                            end_date: endDate,
                            commodity: this.commodity,
                            prompt_type: "analysis"
                        })
                    });

                    if (response.status === 200) {
                        const data = await response.json();
                        generatedText.value = data.generatedText; // Assuming 'generatedText' is a key in your response JSON
                    } else {
                        generatedText.value = "Error: Unable to generate text: " + response.status;
                    }
                } catch (error) {
                    console.error("Fetch error:", error);
                    generatedText.value = "Network error: " + error.message;
                }
            });

            const forecastButton = this.shadowRoot.getElementById("forecast-button");
            forecastButton.addEventListener("click", async () => {
                //const startDate = this.convertDate()
                const endDate = this.convertDate(this.shadowRoot.getElementById("forecast-date").value);
                const generatedText = this.shadowRoot.getElementById("generated-text");
                generatedText.value = "Forecast in progress...";
                // Implement the forecast logic and fetch call here
                try {
                    const response = await fetch("https://finaigpt-public.eu.ngrok.io/generate_response", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            // Add any additional headers your backend requires
                        },
                        body: JSON.stringify({
                            start_date: "31-12-2023", //Aktueller Stand der Database
                            end_date: endDate,
                            commodity: this.commodity,
                            prompt_type: "forecast"
                        })
                    });

                    if (response.status === 200) {
                        const data = await response.json();
                        generatedText.value = data.generatedText; // Assuming 'generatedText' is a key in your response JSON
                    } else {
                        generatedText.value = "Error: Unable to generate text: " + response.status;
                    }
                } catch (error) {
                    console.error("Fetch error:", error);
                    generatedText.value = "Network error: " + error.message;
                }
            });
            const resetButton = this.shadowRoot.getElementById("reset-button");
            resetButton.addEventListener("click", () => {
                const generatedText = this.shadowRoot.getElementById("generated-text");
                generatedText.value = "";
            });
        }

        convertDate(inputFormat) {
            return inputFormat.replace(/\./g, '-');
        }

        onCustomWidgetBeforeUpdate(changedProperties) {
            this._props = {
                ...this._props,
                ...changedProperties
            };
        }

        onCustomWidgetAfterUpdate(changedProperties) {
            this.initMain();
        }
    }

    customElements.define("finai-chatgpt-widget", Widget);
})();
