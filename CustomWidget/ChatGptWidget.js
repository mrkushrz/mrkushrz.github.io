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
        max-width: 630px;
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
    <div class="question-container">
            <textarea id="question-text" rows="4" placeholder="Enter your question here..."></textarea>
            <button id="send-button">Send</button>
    </div>
</div>
    `;

    class Widget extends HTMLElement {
        constructor() {
            super();
            let shadowRoot = this.attachShadow({mode: "open"});
            shadowRoot.appendChild(template.content.cloneNode(true));
            this._props = {};
            this.generatedPrompt = [];
            this.commodity = "globalsugar";
        }

        async connectedCallback() {
            this.init();
        }

        async setCommodity(newValue){
            return this.commodity = newValue;
        }

        async init() {
            const analysisButton = this.shadowRoot.getElementById("analysis-button");
            analysisButton.addEventListener("click", async () => {
                const startDate = this.convertDate(this.shadowRoot.getElementById("start-date").value);
                const endDate = this.convertDate(this.shadowRoot.getElementById("end-date").value);
                const commodity = this.commodity;
                if (!this.validateInput(startDate, endDate, "analysis", commodity)) {
                    return; // Stop execution if validation fails
                }
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
                            commodity: commodity,
                            prompt_type: "analysis"
                        })
                    });

                    if (response.status === 200) {
                        const data = await response.json();
                        const [generatedPrompt, generatedText] = data.generatedResponse;
                        const generatedTextElement = this.shadowRoot.getElementById("generated-text");
                        generatedTextElement.value = generatedText;
                        this.generatedPrompt = generatedPrompt;
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
                const commodity = this.commodity;
                if (!this.validateInput("2023-12-31", endDate, "forecast", commodity)) {
                    return; // Stop execution if validation fails
                }
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
                            start_date: "2023-12-31", //Aktueller Stand der Database
                            end_date: endDate,
                            commodity: commodity,
                            prompt_type: "forecast"
                        })
                    });

                    if (response.status === 200) {
                        const data = await response.json();
                        const [generatedPrompt, generatedText] = data.generatedResponse;
                        const generatedTextElement = this.shadowRoot.getElementById("generated-text");
                        generatedTextElement.value = generatedText;
                        this.generatedPrompt = generatedPrompt;
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
            // Event listener for the Send button
            const sendButton = this.shadowRoot.getElementById('send-button');
            sendButton.addEventListener('click', async () => {
                const generatedText = this.shadowRoot.getElementById(/* ID of your generated text element */).value;
                const question = this.shadowRoot.getElementById('question-text').value;
                if (!question) {
                    alert('Frage zum Output?');
                    return;
                }
                try {
                    const response = await fetch("https://finaigpt-public.eu.ngrok.io/generate_conversation", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            generatedPrompt: this.generatedPrompt,
                            generatedText: generatedText,
                            question: question,
                        })
                    });
                    if (response.status === 200) {
                        const data = await response.json();
                        generatedText.value = data.generatedResponse;
                    } else {
                        alert('Error: ' + response.statusText);
                    }
                } catch (error) {
                    console.error("Error:", error);
                    alert("Error: " + error.message);
                }
            });
        }

        convertDate(inputFormat) {
            return inputFormat.replace(/\./g, '-');
        }
        validateInput(startDate, endDate, promptType, commodity) {
            let startDateObj = new Date(startDate);
            let endDateObj = new Date(endDate);
            const generatedText = this.shadowRoot.getElementById("generated-text");
        
            // Check for prompt type and date conditions
            if (promptType === 'forecast' && endDateObj < new Date('2023-12-31')) {
                generatedText.value = 'End date must be after 01.01.2024 for forecasts.';
                return false;
            }
            if (startDateObj > endDateObj) {
                generatedText.value ='Start date must be before end date.';
                return false;
            }
            if (promptType === 'analysis' && startDateObj < new Date('2023-01-01')) {
                generatedText.value = 'Start date must be after 01.01.2023 for analysis.';
                return false;
            }
            if (promptType === 'analysis' && endDateObj > new Date('2023-12-31')) {
                generatedText.value = 'End date must be before 31.12.2023 for analysis.';
                return false;
            }
            if (! (commodity === 'globalsugar' || commodity === 'europeansugar')){
                generatedText.value = 'Choose commodity';
                return false;
            }
            return true;
        }

        onCustomWidgetBeforeUpdate(changedProperties) {
            if (changedProperties.hasOwnProperty("Commodity")) {
                this.commodity = changedProperties["Commodity"];
            }

            this._props = {
                ...this._props,
                ...changedProperties
            };
        }

        onCustomWidgetAfterUpdate(changedProperties) {
            //this.initMain();
        }
    }

    customElements.define("finai-chatgpt-widget", Widget);
})();
