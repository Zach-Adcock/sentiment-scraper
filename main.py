import pprint
from reddit_comments import get_reddit_comments
from llm_sentiment import filter_comments

keyword = "microsoft"

# Get a list of reddit comments using Google search API and custom engine
reddit_comments = get_reddit_comments(keyword)

# Use openAI to verify that comments are voicing sentiment/opinion on keyword
filtered_comments = filter_comments(reddit_comments, keyword)

for comment in filtered_comments:
    print(comment)
