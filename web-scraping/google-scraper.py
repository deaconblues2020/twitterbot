import json
import requests
from bs4 import BeautifulSoup

print("hi")
def getNewsData():
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

#def get_article_contents(link):



#print("hi again")

news_results = getNewsData()

# Iterating through the list of dictionaries
#for dictionary in news_results:
#    #print(dictionary)
#    link = dictionary["link"]
#    print(link)
link1 = news_results[1]

print("link 1 = " + link1["link"])