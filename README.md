# News without ads 📰

An ad-free, high-speed multi-source news aggregator and cleaner powered by Python and Streamlit. Designed to deliver a distraction-free reading experience across global reference topics.

---

## ✨ Key Features

- **Zero Ads & Clutter:** Strips away banners, trackers, and unnecessary HTML elements using custom text cleaning rules.
- **Dynamic Appearance Theme:** Instantly switch between **☀️ Light Mode** and **🌙 Dark Mode** directly from the sidebar.
- **Bilingual Interface:** Fully localized in English for a clean, global user experience.
- **Optimized RSS Feeds:** Carefully curated, tested, and reliable sources across multiple categories to prevent broken links.
- **Full Article Reader:** Extract and structure full article texts and main cover images on-demand.

---

## 📂 Project Structure

```text
news-cleaner-feed/
│
├── cleaner/
│   └── text_cleaner.py     # Strips out ads, banners, and unwanted tags
├── fetchers/
│   └── rss_fetcher.py      # Handles robust RSS connection and requests
├── app.py                  # Main Streamlit web application interface
├── main.py                 # Console utility for quick feed testing
├── requirements.txt        # Project dependencies
└── README.md               # Documentation

🚀 Getting Started Locally   
1 Clone the repository:

Bash
git clone [https://github.com/Proyecto-Laboratorios-Publicos/news-cleaner-feed.git](https://github.com/Proyecto-Laboratorios-Publicos/news-cleaner-feed.git)
cd news-cleaner-feed

2 Install dependencies:

Bash
pip install -r requirements.txt

3 Run the Streamlit application:

Bash
streamlit run app.py


🌐 Categories & Covered Topics
Technology: TechCrunch, The Verge, Wired, Ars Technica, Engadget, and more.

Finance and Economics: CNBC Markets, Business Insider, Seeking Alpha, SEC News.

Policy: BBC News, The Guardian, Al Jazeera, France 24, UN News.

Entertainment & Culture: Variety, The Hollywood Reporter, Rolling Stone, Smithsonian.

Science, Health & Sports: Nature, Live Science, BBC Sport, Marca, Sky Sports.


