(function() { 
    let template = document.createElement("template");
    template.innerHTML = `
    <style>
    :host {
        border-radius: 25px;
        border-width: 4px;
        border-color: black;
        border-style: solid;
        display: block;
        overflow: auto; /* To handle scrolling if many news items */
    }
    .news-container {
        margin: 20px;
        padding: 10px;
    }
    .news-item {
        margin-bottom: 20px;
        padding: 10px;
        border-bottom: 1px solid #eee;
    }
    .news-title {
        font-size: 18px;
        font-weight: bold;
    }
    .news-description {
        font-size: 14px;
    }
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
            this.commodity = "example"; // Default commodity
            this.fetchNews(); // Fetch news on load

            // Refresh button event listener
            const refreshButton = this.shadowRoot.querySelector('.refresh-button');
            refreshButton.addEventListener('click', () => this.fetchNews());
        }

        async setCommodity(newValue){
            this.commodity = newValue;
            this.fetchNews(); // Fetch news when commodity is set
        }

        fetchNews() {
            const apiKey = 'fb3acf0d177cc306f0e78c3d427c8116';
            const commodity = this.commodity;
            const apiUrl = 'https://gnews.io/api/v4/search?q=${commodity}&max=5&apikey=${apiKey}';

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
            articles.forEach(article => {
                const newsItem = document.createElement('div');
                newsItem.className = 'news-item';
                newsItem.innerHTML = `
                    <div class="news-title">${article.title}</div>
                    <div>By ${article.author}</div>
                    <div class="news-description">${article.description}</div>
                    <a href="${article.url}" target="_blank">Read more</a>
                `;
                container.appendChild(newsItem);
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
