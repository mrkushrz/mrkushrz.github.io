(function () {
    let template = document.createElement("template");
    template.innerHTML = `
        <style>
          :host {}
    
    /* Style for the container */
    div {
      margin: 50px auto;
      max-width: 600px;
    }
    
    /* Style for the input container */
    .input-container {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }
    
    /* Style for the input field */
    #prompt-input {
      padding: 10px;
      font-size: 16px;
      border: 1px solid #ccc;
      border-radius: 5px;
      width: 70%;
    }
    
    /* Style for the button */
    #generate-button {
      padding: 10px;
      font-size: 16px;
      background-color: #3cb6a9;
      color: #fff;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      width: 25%;
    }
    
    /* Style for the generated text area */
    #generated-text {
      padding: 10px;
      font-size: 16px;
      border: 1px solid #ccc;
      border-radius: 5px;
    width:96%;
    }
        </style>
       <div>
    <center>
    <img src="https://1000logos.net/wp-content/uploads/2023/02/ChatGPT-Emblem.png" width="200"/>
    <h1>ChatGPT</h1></center>
    <div class="input-container">
        <input type="date" id="start-date" placeholder="Start Date">
        <input type="date" id="end-date" placeholder="End Date">
        <input type="text" id="commodity-input" placeholder="Enter Commodity">
        <input type="text" id="prompt-input" placeholder="Enter a prompt">
        <button id="generate-button">Generate Text</button>
    </div>
      <textarea id="generated-text" rows="10" cols="50" readonly></textarea>
    </div>
      `;
    class Widget extends HTMLElement {
      constructor() {
        super();
        let shadowRoot = this.attachShadow({
          mode: "open"
        });
        shadowRoot.appendChild(template.content.cloneNode(true));
        this._props = {};
      }
      async connectedCallback() {
        this.init();
      }
      async init() {
        const generateButton = this.shadowRoot.getElementById("generate-button");
        generateButton.addEventListener("click", async () => {
            const startDate = this.shadowRoot.getElementById("start-date").value;
            const endDate = this.shadowRoot.getElementById("end-date").value;
            const commodity = this.shadowRoot.getElementById("commodity-input").value;
            const prompt = this.shadowRoot.getElementById("prompt-input").value;
            const generatedText = this.shadowRoot.getElementById("generated-text");
            generatedText.value = "Finding result...";
    
            try {
                const response = await fetch("https://localhost-public.eu.ngrok.io", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        // Add any additional headers your backend requires
                    },
                    body: JSON.stringify({
                        start_date: startDate,
                        end_date: endDate,
                        commodity: commodity,
                        prompt: prompt
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
    customElements.define("FinAIChatGptWidget", Widget);
  })();
  