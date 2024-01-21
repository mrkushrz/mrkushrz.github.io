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
        </style> 
        <div class="news-container"></div>
    `;

    class NewsHeadlines extends HTMLElement {
        constructor() {
            super(); 
            this.attachShadow({mode: "open"});
            this.shadowRoot.appendChild(template.content.cloneNode(true));
            this._props = {};

            this.fetchNews();
        }

        fetchNews() {
            const apiKey = '08d5a12af6af43229edc915e160819a5';
            const apiUrl = `https://newsapi.org/v2/top-headlines?q=sugar&apiKey=${apiKey}`;

            fetch(apiUrl)
                .then(response => response.json())
                .then(data => this.displayNews(data.articles))
                .catch(error => console.error('Error fetching news:', error));
        }

        displayNews(articles) {
            const container = this.shadowRoot.querySelector('.news-container');
            articles.slice(0, 5).forEach(article => {
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