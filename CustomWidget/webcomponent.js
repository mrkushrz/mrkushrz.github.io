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
    this.attachShadow({ mode: "open" }).appendChild(template.content.cloneNode(true));
    this._props = {};
    this.initElements();
  }

  initElements() {
    this.analysisButton = this.shadowRoot.getElementById("analysis-button");
    this.forecastButton = this.shadowRoot.getElementById("forecast-button");
    this.generatedText = this.shadowRoot.getElementById("generated-text");
    this.commodityInput = this.shadowRoot.getElementById("commodity-input");
    this.startDateInput = this.shadowRoot.getElementById("start-date");
    this.endDateInput = this.shadowRoot.getElementById("end-date");
    this.forecastDateInput = this.shadowRoot.getElementById("forecast-date");
    this.forecastingPeriodInput = this.shadowRoot.getElementById("forecasting-period");
  }

  connectedCallback() {
    this.analysisButton.addEventListener("click", () => this.handleAnalysis());
    this.forecastButton.addEventListener("click", () => this.handleForecast());
  }

  disconnectedCallback() {
    this.analysisButton.removeEventListener("click", this.handleAnalysis);
    this.forecastButton.removeEventListener("click", this.handleForecast);
  }

  async fetchData(endpoint, body) {
    this.generatedText.value = `${body.type.charAt(0).toUpperCase() + body.type.slice(1)} in progress...`;
    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });

      if (response.status === 200) {
        const data = await response.json();
        this.generatedText.value = data.generatedText;
      } else {
        this.generatedText.value = "Error: Unable to generate text";
      }
    } catch (error) {
      console.error("Fetch error:", error);
      this.generatedText.value = "Network error";
    }
  }

  async handleAnalysis() {
    const startDate = this.convertDate(this.startDateInput.value);
    const endDate = this.convertDate(this.endDateInput.value);
    const commodity = this.commodityInput.value;
    await this.fetchData("https://localhost-public.eu.ngrok.io", {
      start_date: startDate,
      end_date: endDate,
      commodity: commodity,
      type: "analysis"
    });
  }

  async handleForecast() {
    const forecastDate = this.convertDate(this.forecastDateInput.value);
    const forecastingPeriod = this.forecastingPeriodInput.value;
    const commodity = this.commodityInput.value;
    await this.fetchData("https://localhost-public.eu.ngrok.io", {
      forecast_date: forecastDate,
      forecasting_period: forecastingPeriod,
      commodity: commodity,
      type: "forecast"
    });
  }

  convertDate(inputFormat) {
    return inputFormat.replace(/\./g, '/');
  }

  onCustomWidgetBeforeUpdate(changedProperties) {
    this._props = { ...this._props, ...changedProperties };
  }

  onCustomWidgetAfterUpdate(changedProperties) {
    this.initElements();
  }
}

customElements.define("finai-chatgpt-widget", Widget);
})();
