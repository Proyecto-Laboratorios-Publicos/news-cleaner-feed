from fetchers.rss_fetcher import RSSFetcher
from cleaner.text_cleaner import TextCleaner

# Master dictionary of categories and their specialized RSS feeds
CATEGORIES = {
    "1": {
        "name": "Technology", 
        "url": "https://techcrunch.com/feed/"
    },
    "2": {
        "name": "Finance and Economics", 
        "url": "https://markets.businessinsider.com/rss/news"
    },
    "3": {
        "name": "Policy", 
        "url": "https://feeds.bbci.co.uk/news/world/rss.xml"
    },
    "4": {
        "name": "Entertainment", 
        "url": "https://variety.com/feed/"
    }
}

def main():
    print("=== News without ads ===")
    print("Select the category you want to consult:\n")
    
    for key, cat in CATEGORIES.items():
        print(f"[{key}] {cat['name']}")
        
    choice = input("\nEnter the category number: ").strip()
    
    if choice not in CATEGORIES:
        print("[-] Invalid option. Execution finished.")
        return
        
    selected_category = CATEGORIES[choice]
    print(f"\n[+] You selected: {selected_category['name']}")
    
    # Initialize the RSS connector with the specific URL of the selected category
    fetcher = RSSFetcher(source_name=selected_category['name'], endpoint_url=selected_category['url'])
    print(f"Connecting to the {fetcher.source_name} feed...")
    
    # Fetch raw content via requests
    raw_rss_data = fetcher.fetch()
    
    if raw_rss_data:
        print(f"\n[+] Connection successful! Data downloaded ({len(raw_rss_data)} characters).")
        
        # Process and clean content using BeautifulSoup/TextCleaner
        print("\n[+] Processing and cleaning feed content...")
        cleaned_output = TextCleaner.remove_ads_and_banners(raw_rss_data)
        
        print(f"\n--- CLEAN CONTENT: {selected_category['name'].upper()} ---")
        print(cleaned_output[:800] + "...\n[Content truncated for display]")
        print("-------------------------------------------------------------")
    else:
        print("[-] Could not retrieve data from the RSS feed.")
        
    print("\nExecution of main.py finished successfully.")

if __name__ == "__main__":
    main()
