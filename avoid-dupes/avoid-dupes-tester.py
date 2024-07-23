import os

SEEN_LINKS_FILE = 'seen_links_test.txt'


def load_seen_links():
    if not os.path.exists(SEEN_LINKS_FILE):
        return set()
    with open(SEEN_LINKS_FILE, 'r') as file:
        seen_links = {line.strip() for line in file}
    return seen_links


def save_seen_links(seen_links):
    with open(SEEN_LINKS_FILE, 'w') as file:
        for link in seen_links:
            file.write(f"{link}\n")


def mock_fetch_news_data():
    # This function simulates fetching news data
    # Replace this with actual news fetching logic
    return [
        {"link": "https://example.com/article1", "title": "Article 1"},
        {"link": "https://example.com/article2", "title": "Article 2"},
        {"link": "https://example.com/article3", "title": "Article 3"}
    ]


def process_articles():
    seen_links = load_seen_links()
    news_results = mock_fetch_news_data()

    if not news_results:
        print("No news results found.")
        return

    new_links = []
    for article in news_results:
        link = article["link"]
        if link not in seen_links:
            print(f"Processing new article: {link}")
            # Simulate processing the article (e.g., generating tweet message)
            tweet_message = f"New article found: {article['title']}"
            print(tweet_message)
            # Add the link to the seen links set
            seen_links.add(link)
            new_links.append(link)
        else:
            print(f"Skipping already seen article: {link}")

    # Save the updated seen links
    if new_links:
        save_seen_links(seen_links)


if __name__ == "__main__":
    process_articles()
