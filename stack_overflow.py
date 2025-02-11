import requests
import time
from html import unescape


# Fetch stack overflow posts
def fetch_stackoverflow_posts(keyword):
    """
        Searches Stack Overflow's API for post titles containing the 
        given keyword. Returns back a list of dictionaries holding the
        link title and the link URL.
    """

    # Get current time (Unix) and time for 3 months ago to maintain relevance
    current_time = int(time.time())
    three_months_back = current_time - (90 * 24 * 60 * 60)

    params = {
        "site": "stackoverflow",
        "q": keyword,
        "filter": "withbody",
        "title": keyword,
        "fromdate": three_months_back,
    }

    # Send GET request
    API_URL = "https://api.stackexchange.com/2.3/search/advanced"
    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        posts = []

        try:
            for item in data["items"]:
                post_title = item["title"]
                post_url = item["link"]

                # Fetch answers
                # if "answers" in item:
                #     for answer in item["answers"]:
                #         answer_bodies.append(answer["body"])

                posts.append({
                    "title": unescape(post_title),
                    "url": post_url
                })
        except KeyError:
            print("No results found")
        return posts
    else:
        print(f"Error fetching data: {response}")
        return []


