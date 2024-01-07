(function () {
  let template = document.createElement("template");
  template.innerHTML = `
      <style>
        :host {}
  
        div {
          margin: 50px auto;
          max-width: 600px;
        }
  
        .input-container {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 20px;
        }
  
        input {
          padding: 10px;
          font-size: 16px;
          border: 1px solid #ccc;
          border-radius: 5px;
          width: 70%;
        }
  
        button {
          padding: 10px;
          font-size: 16px;
          background-color: #3cb6a9;
          color: #fff;
          border: none;
          border-radius: 5px;
          cursor: pointer;
          width: 25%;
        }
  
        textarea {
          padding: 10px;
          font-size: 16px;
          border: 1px solid #ccc;
          border-radius: 5px;
          width: 96%;
        }
      </style>
      <div>
        <center>
          <img src="https://1000logos.net/wp-content/uploads/2023/02/ChatGPT-Emblem.png" width="200"/>
          <h1>ChatGPT</h1>
        </center>
        <div class="input-container" id="commodity-container">
          <select id="commodity-input">
            <option value="globalsugar">Global Sugar</option>
            <option value="europeansugar">European Sugar</option>
          </select>
        </div>
        <div class="input-container" id="analysis-container">
          <input type="date" id="start-date" placeholder="Start Date">
          <input type="date" id="end-date" placeholder="End Date">
          <button id="analysis-button">Analysis</button>
        </div>
        <div class="input-container" id="forecast-container">
          <input type="date" id="forecast-date" placeholder="Start Date">
          <select id="forecasting-period">
            <option value="week">Week</option>
            <option value="month">Month</option>
            <option value="year">Year</option>
          </select>
          <button id="forecast-button">Forecast</button>
        </div>
        <textarea id="generated-text" rows="10" cols="50" readonly></textarea>
      </div>
    `;
  class Widget extends HTMLElement {
    constructor() {
      super();
      let shadowRoot = this.attachShadow({ mode: "open" });
      shadowRoot.appendChild(template.content.cloneNode(true));
      this._props = {};
    }
    async connectedCallback() {
      this.init();
    }
    async init() {
      const analysisButton = this.shadowRoot.getElementById("analysis-button");
      analysisButton.addEventListener("click", async () => {
          const startDate = this.convertDate(this.shadowRoot.getElementById("start-date").value);
          const endDate = this.convertDate(this.shadowRoot.getElementById("end-date").value);
          const commodity = this.shadowRoot.getElementById("commodity-input").value;
          const generatedText = this.shadowRoot.getElementById("generated-text");
          generatedText.value = "Analysis in progress...";
          // Implement the analysis logic and fetch call here
		  try {
					const response = await fetch(" https://localhost-public.eu.ngrok.io/generate_response", {
						method: "POST",
						headers: {
							"Content-Type": "application/json",
							// Add any additional headers your backend requires
						},
						body: JSON.stringify({
							start_date: startDate,
							end_date: endDate,
							commodity: commodity,
							type: "analysis"
						})
					});
		
					if (response.status === 200) {
						const data = await response.json();
						generatedText.value = data.generatedText; // Assuming 'generatedText' is a key in your response JSON
					} else {
						generatedText.value = "Error: Unable to generate text";
					}
				} catch (error) {
					console.error("Fetch error:", error);
					generatedText.value = "Network error";
				}
			});
	  });

      const forecastButton = this.shadowRoot.getElementById("forecast-button");
      forecastButton.addEventListener("click", async () => {
          const forecastDate = this.convertDate(this.shadowRoot.getElementById("forecast-date").value);
          const forecastingPeriod = this.shadowRoot.getElementById("forecasting-period").value;
		  const commodity = this.shadowRoot.getElementById("commodity-input").value;
          const generatedText = this.shadowRoot.getElementById("generated-text");
          generatedText.value = "Forecast in progress...";
          // Implement the forecast logic and fetch call here
		  try {
					const response = await fetch(" https://localhost-public.eu.ngrok.io/generate_response", {
						method: "POST",
						headers: {
							"Content-Type": "application/json",
							// Add any additional headers your backend requires
						},
						body: JSON.stringify({
							forecast_date: forecastDate,
							forecasting_period: forecastingPeriod,
							commodity: commodity,
							type: "forecast"
						})
					});
		
					if (response.status === 200) {
						const data = await response.json();
						generatedText.value = data.generatedText; // Assuming 'generatedText' is a key in your response JSON
					} else {
						generatedText.value = "Error: Unable to generate text";
					}
				} catch (error) {
					console.error("Fetch error:", error);
					generatedText.value = "Network error";
				}		
	  });
    }

    convertDate(inputFormat) {
      return inputFormat.replace(/\./g, '/');
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
