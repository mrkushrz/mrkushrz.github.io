(function() { 
    let template = document.createElement("template");
    template.innerHTML = `
        <style>
            /* ... existing styles ... */
            .refresh-button {
                margin: 10px;
                padding: 5px 10px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
        </style> 
        <div class="news-container"></div>
        <button class="refresh-button">Refresh News</button>
    `;

    class NewsHeadlines extends HTMLElement {
        constructor() {
            super(); 
            this.attachShadow({mode: "open"});
            this.shadowRoot.appendChild(template.content.cloneNode(true));
            this._props = {};

            this.fetchNews();

            // Refresh button event listener
            const refreshButton = this.shadowRoot.querySelector('.refresh-button');
            refreshButton.addEventListener('click', () => this.refreshNews());
        }

        fetchNews() {
            const apiKey = '08d5a12af6af43229edc915e160819a5';
            const apiUrl = `https://newsapi.org/v2/top-headlines?q=sugar&apiKey=${apiKey}`;

            fetch(apiUrl)
                .then(response => response.json())
                .then(data => this.displayNews(data.articles))
                .catch(error => console.error('Error fetching news:', error));
        }

        refreshNews() {
            // Clear existing news items
            const container = this.shadowRoot.querySelector('.news-container');
            container.innerHTML = '';

            // Fetch and display new news items
            this.fetchNews();
        }

        displayNews(articles) {
            const container = this.shadowRoot.querySelector('.news-container');
            articles.slice(0, 5).forEach(article => {
                // ... existing code ...
            });
        }

        onCustomWidgetBeforeUpdate(changedProperties) {
            this._props = { ...this._props, ...changedProperties };
        }

        onCustomWidgetAfterUpdate(changedProperties) {
            if ("color" in changedProperties) {
                this.style["background-color"] = changedProperties["color"];
            }
            if ("opacity" in changedProperties) {
                this.style["opacity"] = changedProperties["opacity"];
            }
        }
    }

    customElements.define("news-table-widget", NewsHeadlines);
})();
