import praw
from dotenv import load_dotenv
import os
import requests
import pprint

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_SECRET"),
    user_agent="sentiment comments from keywords"
)


def google_search(keyword):
    params = {
        "q": f'site:reddit.com inurl:comments "{keyword}"',
        "key": os.getenv("GOOGLE_API_KEY"),
        "cx": os.getenv("GOOGLE_CSE_ID"),
        "num": 10,
        "dateRestrict":  'm3',
    }

    url_base = "https://www.googleapis.com/customsearch/v1"
    response = requests.get(url_base, params=params)
    results = response.json()

    return results


def urls_and_ids(res_list):
    '''  
    Takes a JSON object that includes reddit links. 
    Returns a list of lists with the urls and reddit link IDs
    '''
    url_list = []   # list of lists [post_url, post_id]
    try:
        for page in res_list['items']:
            if page['link'] and 'comments' in page['link']:
                # Get reddit post ID from the URL
                url = page['link']
                start_ind = url.find("comments/") + 9   # 8 is len of "comments/"
                end_ind = url.find("/", start_ind)
                reddit_post_id = url[start_ind:end_ind]
                # print("reddit_post_id: ", reddit_post_id)

                url_list.append([url, reddit_post_id])
            elif page['link']:
                url_list.append([page['link'], ""])

            else:
                continue

    except KeyError:
        print("No Results Found for this keyword")
        
    return url_list


def reddit_comments_from_submission(reddit_submission_id, reddit_submission_url, reddit_comments, keyword):
    submission = reddit.submission(reddit_submission_id)
    submission.comments.replace_more(limit=0)
    for top_level_comment in submission.comments:
        if keyword.lower() in top_level_comment.body or keyword.upper() in top_level_comment.body:
            reddit_comments.append({'comment': top_level_comment.body, "url": reddit_submission_url})
    
    return reddit_comments


def get_reddit_comments(keyword):
    res_list = google_search(keyword)
    reddit_urls = urls_and_ids(res_list)
    reddit_comments = []

    for reddit_submission in reddit_urls:
        reddit_comments_from_submission(reddit_submission[1], reddit_submission[0], reddit_comments, keyword)

    if reddit_comments:
        return reddit_comments
    else:
        return ["No relevant results found for this keyword"]
