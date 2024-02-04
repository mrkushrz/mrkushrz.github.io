(function() { 
    let template = document.createElement("template");
    template.innerHTML = `
    <style>
    :host {
        border-radius: 25px;
        border-width: 4px;
        display: block;
        overflow: auto; /* To handle scrolling if many news items */
    }
    .news-container {
        padding: 5px;
    }
    .news-item {
        padding: 5px;
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
        padding: 7px;
        background-color: #000000;
        color: white;
        border: none;
        border-radius: 50px;
        cursor: pointer;
        font-size: 18px;
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
            this.commodity = "globalsugar"; // Default commodity
            this.fetchNews(); // Fetch news on load

            // Refresh button event listener
            const refreshButton = this.shadowRoot.querySelector('.refresh-button');
            refreshButton.addEventListener('click', () => this.refreshNews());
        }

        setCommodity(newValue){
            this.commodity = newValue;
            this.refreshNews(); // Fetch news when commodity is set
        }

        fetchNews() {
            const apiKey = '9Td6Yigy6JupD89A8KcNuZUZUaUCBKvKnWFpyvge';
            let commodity = this.commodity;

            // Replace 'globalsugar' with 'global+sugar'
            if (commodity === "globalsugar") {
                commodity = "global+sugar";
            }
            // Replace 'europeansugar' with 'european+sugar'
            if (commodity === "europeansugar") {
                commodity = "european+sugar";
            }
            const apiUrl = `https://api.marketaux.com/v1/news/all?api_token=${apiKey}&search=${commodity}&language=en&limit=3`;

            fetch(apiUrl)
                .then(response => response.json())
                .then(data => this.displayNews(data.data))
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
                    <div class="news-description">${article.description}</div>
                    <a href="${article.url}" target="_blank">Link</a>
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
