from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def filter_titles(post_list, keyword, site):
    filtered_posts = []

    prompt_prefix = f"""The following is an article
    from the website: {site}. Return "True"
    if the title includes an opinion or sentiment 
    (either positive or negative) about {keyword}.
    If the comment does not include the {keyword}, or
    does not imply an opinion about {keyword} return
    "False". Be strict with your decisions to make sure
    the "True" comments are opinionated.
    """

    for post in post_list:
        prompt = prompt_prefix + post['title']
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": f"You will read article and post titles from {site} website and filter out all titles that do not express any sentiment about {keyword}."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        opinionated_post = response.choices[0].message.content.lower()
        if opinionated_post == "true":
            filtered_posts.append(post)

    return filtered_posts