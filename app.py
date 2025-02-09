import pprint
from reddit_comments import get_reddit_comments
from stack_overflow import fetch_stackoverflow_posts
from llm_sentiment import filter_comments
from hackernews import fetch_hackernews_posts
from flask import Flask, render_template, request, redirect, url_for, g
import secrets


app = Flask(__name__)
# app.secret_key = secrets.token_urlsafe(32)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def fetch_quotes():
    keyword = request.form.get("keyword")
    sites = request.form.getlist("sites")

    reddit_quotes = []
    # If Reddit selected for search
    if "reddit" in sites:
        # Get a list of reddit comments using Google search API and custom engine
        reddit_comments = get_reddit_comments(keyword)

        # Use openAI to verify that comments are voicing sentiment/opinion on keyword
        reddit_quotes = filter_comments(reddit_comments, keyword)

        # Display quotes on results page
    
    stack_overflow_posts = []
    # If Stack Overflow selected in search
    if "stack_overflow" in sites:
        # Get a list of Stack overflow posts
        stack_overflow_posts = fetch_stackoverflow_posts(keyword)
    
    hackernews_articles = []
    # If Hacker news selected in search
    if "hackernews" in sites:
        # Get a list of Hackernews articles
        hackernews_articles = fetch_hackernews_posts(keyword)


    return render_template(
                            "display_quotes.html",
                            keyword=keyword, 
                            reddit_quotes=reddit_quotes,
                            stack_overflow_posts=stack_overflow_posts,
                            fetch_hackernews_posts=hackernews_articles,
                            sites=sites
                            )

    
    # return redirect(url_for("results"))


# @app.route("/results", methods=["GET"])
# def results():
#     keyword = getattr(g, "keyword", "")
#     print("kewyord: ", keyword)
#     reddit_quotes = getattr(g, "reddit_quotes", [])
#     stack_overflow_posts = getattr(g, "stack_overflow_posts", [])
    

if __name__ == "__main__":
    app.run(debug=True)


# keyword = "microsoft"


# for comment in filtered_comments:
#     print(comment)
