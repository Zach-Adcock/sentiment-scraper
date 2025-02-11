from reddit_comments import get_reddit_comments
from stack_overflow import fetch_stackoverflow_posts
from reddit_llm_sentiment import filter_comments
from llm_sentiment import filter_titles
from hackernews import fetch_hackernews_posts
from heroku_db import connect_heroku_db

from flask import Flask, render_template, request, redirect, url_for
import uuid
import json
import pprint


app = Flask(__name__)

# Connect to Heroku SQL database
connection, cursor = connect_heroku_db()

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def fetch_quotes():
    keyword = request.form.get("keyword")
    sites = request.form.getlist("sites")

    reddit_quotes = []
    if "reddit" in sites:
        # Get a list of reddit comments using Google search API and custom engine
        reddit_comments = get_reddit_comments(keyword)

        # Use openAI to verify that comments are voicing sentiment/opinion on keyword
        reddit_quotes = filter_comments(reddit_comments, keyword)

    stack_overflow_posts = []
    if "stack_overflow" in sites:
        # Get a list of Stack overflow posts
        posts = fetch_stackoverflow_posts(keyword)
        stack_overflow_posts = filter_titles(posts, keyword, "stack_overflow")
    
    hackernews_articles = []
    if "hackernews" in sites:
        # Get a list of Hackernews articles
        articles = fetch_hackernews_posts(keyword)
        hackernews_articles = filter_titles(articles, keyword, "hackernews")
    
    # Save search info for redirect to /results
    search_id = str(uuid.uuid4())
    results = {
        "reddit_quotes": reddit_quotes,
        "stack_overflow_posts": stack_overflow_posts,
        "hackernews_articles": hackernews_articles,
        "sites": sites
    }

    try:
        cursor.execute(
            "INSERT INTO search_results (search_id, keyword, results) VALUES (%s, %s, %s) ON CONFLICT (search_id) DO NOTHING",
            (search_id, keyword, json.dumps(results)) 
        )
        connection.commit()
    except Exception:
        print("Could not save data.")

    return redirect(url_for("results", search_id=search_id))


@app.route("/results", methods=["GET"])
def results():
    search_id = request.args.get("search_id")
    data = ""

    # Fetch results JSON from db
    try:
        cursor.execute("SELECT keyword, results FROM search_results WHERE search_id = %s", (search_id,))
        data = cursor.fetchone()
    except Exception as error:
        print(error)
        print(f"Unable to get results for search_id: {search_id}")

    if data:
        keyword, results = data
        
        # unpack results
        reddit_quotes = results.get('reddit_quotes', [])
        stack_overflow_posts = results.get('stack_overflow_posts', [])
        hackernews_articles = results.get('hackernews_articles', [])
        sites = results.get('sites', [])

    return render_template(
                    "display_quotes.html", 
                    keyword=keyword, 
                    reddit_quotes=reddit_quotes,
                    stack_overflow_posts=stack_overflow_posts,
                    hackernews_articles=hackernews_articles,
                    sites=sites
                )


if __name__ == "__main__":
    app.run(debug=True)

