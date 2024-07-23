import requests
import json
from openai import OpenAI
client = OpenAI()
from bs4 import BeautifulSoup
from requests_oauthlib import OAuth1Session
import os

consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

SEEN_LINKS_FILE = 'seen_links.txt'

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



def get_news_data():
    headers = {
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    }
    cookies = {
        "CONSENT": "PENDING+987",
        "SOCS": "CAESHAgBEhJnd3NfMjAyMzA4MTAtMF9SQzIaAmRlIAEaBgiAo_CmBg"
    }
    response = requests.get(
        #"https://www.google.com/search?q=us+stock+markets&gl=us&tbm=nws&num=100", headers=headers, cookies = cookies
        "https://www.google.com/search?q=A.i.&hl=en-US&gl=us&tbm=nws&num=100", headers=headers, cookies = cookies
    )
    soup = BeautifulSoup(response.content, "html.parser")
    news_results = []

    for el in soup.select("div.SoAPf"):

        try:
            linkinfo = el.parent.parent.parent.find("a")["href"]
        except AttributeError as ae:
            print("problem with link info")
            linkinfo = ""

        try:
            titleinfo = el.select_one("div.n0jPhd").get_text()
        except AttributeError as ae:
            print("problem with title info")
            titleinfo = ""

        try:
            snippetinfo = el.select_one(".GI74Re").get_text()
        except AttributeError as ae:
            print("problem with snippet info")
            snippetinfo = ""

        try:
            dateinfo = el.select_one(".LfVVr").get_text()
        except AttributeError as ae:
            print("problem with date info")
            dateinfo = ""

        try:
            sourceinfo = el.select_one(".NUnG9d span").get_text()
        except AttributeError as ae:
            print("problem with source info")
            sourceinfo = ""

        news_results.append(
            {
                "link": linkinfo,
                "title": titleinfo,
                "snippet": snippetinfo,
                "date": dateinfo,
                "source": sourceinfo
            }
        )
    #print(json.dumps(news_results, indent=2))

    return news_results


def call_openai(link):
    try:
      completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
          # {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
          {"role": "user",
           "content": "Here is a link to an article : " + link + ". Summarize this article in a tweet. This tweet should be limited be less than 260 characters. please include the link to the article"}
        ]
      )

      return completion.choices[0].message.content
    except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return ""



def send_tweet(tweet_message):
    # Be sure to add replace the text of the with the text you wish to Tweet. You can also add parameters to post polls, quote Tweets, Tweet with reply settings, and Tweet to Super Followers in addition to other features.
    payload = {"text": tweet_message}

    # Make the request
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    # Making the request
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )

    if response.status_code != 201:
        raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )

    print("Response code: {}".format(response.status_code))

    # Saving the response as JSON
    json_response = response.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))


def main():
    news_results = get_news_data()
    if not news_results:
        print("No news results found.")
        return

    seen_links = load_seen_links()
    new_links = []
    for article in news_results:
        link = article["link"]
        if link not in seen_links:
            print(f"Processing new article: {link}")
            # Simulate processing the article (e.g., generating tweet message)
            tweet_message = f"New article found: {article['title']}"

            tweet_message = call_openai(link)
            print(tweet_message)
            if tweet_message:
                print(f"tweet_message = {tweet_message}")
                send_tweet(tweet_message)
            else:
                print("Failed to generate tweet message.")

            # Add the link to the seen links set
            seen_links.add(link)
            new_links.append(link)
            if new_links:
                save_seen_links(seen_links)

            return
        else:
            print(f"Skipping already seen article: {link}")



if __name__ == "__main__":
    main()
