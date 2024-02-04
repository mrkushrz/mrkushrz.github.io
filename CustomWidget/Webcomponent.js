(function () {
    let template = document.createElement("template");
    template.innerHTML = `
 <style>
    table, th, td {
        border: 0px solid black;
    }

    th, td {
        text-align: left;
        padding: 0px; /* Adjust the padding as needed */
        margin: 0; /* Removes any default margins */
    }
    tr {
        margin: 0; /* Removes any default margins */
    }

    .reset-button {
        float: right;
        margin-bottom: 5px; /* Fügt 10px Abstand unter dem Button hinzu */
        background-color: #0c1110; /* Helle Graufarbe */
    }
    

    .input-container > label {
        margin-right: 20px;
    }

    .input-container > input[type="date"], .input-container > button {
        padding: 10px;
        font-size: 16px;
        border: 1px solid #ccc;
        border-radius: 50px;
        margin-top: 5px;
        width: 120px;
    }

    .input-container > input[type="date"] {
        margin-right: 20px;
    }

     
    .button-text {
    margin-left: 10px; /* Passen Sie den Wert nach Bedarf an */
    }

    .input-container > button {
        background-color: #75ac9d;
        color: #fff;
        border: none;
        cursor: pointer;
        padding: 5px 10px; /* Verringert das Padding im Button */
        font-size: 14px; /* Optional: Verkleinert die Schriftgröße, falls nötig */
    }

    .input-container > button:active {
        background-color: #75ac9d;
    }


     
    #send-button {
        background-color: #75ac9d; /* Setzt die Hintergrundfarbe auf #75ac9d */
        font-size: 2px;
        padding: 5px; /* Verringert das Padding im Button */
        font-size: 20px; /* Optional: Verkleinert die Schriftgröße, falls nötig */
    }

    
    #end-date {
    margin-top: 10px; /* Passen Sie den Wert nach Bedarf an */
    margin-left: 5px; /* Füge einen linken Abstand hinzu, um das Feld nach rechts zu verschieben */
    }


    #analysis-button {
    margin-left: 59px; 
    padding: 4px;
    font-size: 20px;
    margin-top: 10px;
    width: 140px;
    }


    #forecast-button {
    margin-left: 118px; /* Erhöht den Abstand nach rechts */
    padding-left: 20px;
    padding: 5px;
    font-size: 20px;
    width: 140px;
    }

    #forecast-date {
    margin-top: 50px; /* Erhöht den Abstand nach unten */
    }

     
    .question-container {
        text-align: central; /* Center-align text within the container */
    }
    
    /* Align the response-text textarea under the question-text */
    .response-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center; /* Center-align text within the container */
    }
    
    #response-text {
        background-color: #f6f6f6; /* Light grey background */
        margin-top: 15px; /* Adds spacing between question-text and response-text */
    }
    
    #question-text{
        width: 60%;
    }
    
    /* Change the background color of the generated-text textarea to light grey */
    #generated-text {
        background-color: #f6f6f6; /* Light grey background */
        margin-bottom:15px;
    }

    
    textarea {
        padding: 30px;
        font-size: 16px;
        border: 1px solid #ccc;
        border-radius: 5px;
        width: 98%;
        width:600px;
        margin-left: 70px;
    }

    button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 7px;
        font-size: 18px;
        background-color: #3cb6a9;
        color: #fff;
        border: none;
        border-radius: 20px;
        cursor: pointer;
    }

    button:active {
        background-color: #2a8076;
    }

    button img {
        width:35px; /* Set image width */
        vertical-align: middle; /* Align image vertically with text */
    }

</style>


<div class="main-container">
    <table>
        <tr>
            <td class="input-container" id="analysis-container">
                <label for="start-date">Start</label>
                <input type="date" id="start-date">
                <br>
                <label for="end-date">End</label>
                <input type="date" id="end-date">
                <br>
                <button id="analysis-button"> 
                    <img
                    src="https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg" 
                    style="float:left; margin-right:0.3em">
                    Analysis
                </button>
            </td>
            <td class="output-container">
                <div class="reset-button-container">
                    <button id="reset-button" class="reset-button">Reset</button>
                </div>
                <textarea id="generated-text" placeholder="GenAI powered Analysis or Trend Forecasting" rows="10" readonly></textarea>
            </td>
        </tr>
        <tr>
            <td class="input-container" id="forecast-container">
                <label for="forecast-date">Forecast End</label>
                <input type="date" id="forecast-date">
                <br>
                <button id="forecast-button" style="margin-top: 10px;"> 
                    <img
                    src="https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg" 
                    style="float:left; margin-right:0.3em">
                    Forecast
                </button>
            </td>
            <td class="question-container">
                <div class="question-input">
                    <textarea id="question-text" rows="4" placeholder="Still Questions?"></textarea>
                    <button id="send-button">
                    <img
                    src="https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg" 
                    style="float:left; margin-right:0.3em">
                    Send</button>
                </div>
                <textarea id="response-text" rows="4" placeholder="GenAI Explanation for your Question" readonly></textarea>
            </td>
        </tr>
    </table>
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
                    return;
                }
                const generatedText = this.shadowRoot.getElementById("generated-text");
                generatedText.value = "Analysis in progress...";
                try {
                    const response = await fetch("https://finaigpt-public.eu.ngrok.io/generate_response", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
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
                        const [generatedMessages, generatedText] = data.generatedResponse;
                        const generatedTextElement = this.shadowRoot.getElementById("generated-text");
                        generatedTextElement.value = generatedText;
                        this.generatedPrompt = generatedMessages;
                        // Show the question container
                        this.showQuestionContainer();
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
                const endDate = this.convertDate(this.shadowRoot.getElementById("forecast-date").value);
                const commodity = this.commodity;
                if (!this.validateInput("2023-12-31", endDate, "forecast", commodity)) {
                    return;
                }
                const generatedText = this.shadowRoot.getElementById("generated-text");
                generatedText.value = "Forecast in progress...";
                try {
                    const response = await fetch("https://finaigpt-public.eu.ngrok.io/generate_response", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({
                            start_date: "2023-12-31",
                            end_date: endDate,
                            commodity: commodity,
                            prompt_type: "forecast"
                        })
                    });

                    if (response.status === 200) {
                        const data = await response.json();
                        const [generatedMessages, generatedText] = data.generatedResponse;
                        const generatedTextElement = this.shadowRoot.getElementById("generated-text");
                        generatedTextElement.value = generatedText;
                        this.generatedPrompt = generatedMessages;
                        // Show the question container
                        this.showQuestionContainer();
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
                // Hide the question container when reset is clicked
                // this.hideQuestionContainer();
            });

            const sendButton = this.shadowRoot.getElementById('send-button');
            sendButton.addEventListener('click', async () => {
                const generatedText = this.shadowRoot.getElementById("generated-text").value;
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
                        // Display the response in the response-text textarea
                        const responseText = this.shadowRoot.getElementById("response-text");
                        responseText.value = data.generatedResponse;
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
            // Check if start date or end date is missing
            if (!startDate && promptType === 'analysis' ) {
                alert('Please enter a start date.');
                return false;
            }
            if (!endDate) {
                alert('Please enter an end date.');
                return false;
            }
        
            let startDateObj = new Date(startDate);
            let endDateObj = new Date(endDate);
            
            // Check for prompt type and date conditions
            if (promptType === 'forecast' && endDateObj < new Date('2023-12-31')) {
                alert('End date must be after 01.01.2024 for forecasts.');
                return false;
            }
            if (startDateObj > endDateObj) {
                alert('Start date must be before end date.');
                return false;
            }
            if (promptType === 'analysis' && startDateObj < new Date('2023-01-01')) {
                alert('Start date must be after 01.01.2023 for analysis.');
                return false;
            }
            if (promptType === 'analysis' && endDateObj > new Date('2023-12-31')) {
                alert('End date must be before 31.12.2023 for analysis.');
                return false;
            }
            if (!(commodity === 'globalsugar' || commodity === 'europeansugar')){
                alert('Choose commodity');
                return false;
            }
            return true;
        }

        showQuestionContainer() {
            const questionContainer = this.shadowRoot.querySelector(".question-container");
            questionContainer.style.display = "block";
        }

        hideQuestionContainer() {
            const questionContainer = this.shadowRoot.querySelector(".question-container");
            questionContainer.style.display = "none";
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

    customElements.define("test-finai-chatgpt-widget", Widget);
})();
