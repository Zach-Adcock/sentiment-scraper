import requests
import time
import pprint


def fetch_hackernews_posts(keyword):
    """
        Utilizes Hackernews API to gather articles that
        feature the keyword that was searched.

        returns [{'title': title, 'url': url}]
    """

    # Get current time (Unix) and time for 3 months ago to maintain relevance
    current_time = int(time.time())
    three_months_back = current_time - (90 * 24 * 60 * 60)


    API_URL = 'http://hn.algolia.com/api/v1/search'
    params = {
        'query': keyword,
        'tags': 'story',
        'numericFilters': f'created_at_i>{three_months_back}',
        'hitsPerPage': 10, 
        'page': 0
    }

    # Make GET request
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        stories = [{"title": hit['title'], "url": hit['url']} for hit in data['hits']]
        return stories
    else:
        print(f"Error: {response}")
        return []


# pprint.pprint(fetch_hackernews_posts("microsoft"))