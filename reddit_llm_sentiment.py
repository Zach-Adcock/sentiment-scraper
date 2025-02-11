from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def filter_comments(post_list, keyword):
    filtered_comments = []

    prompt_prefix = f"""The following is a
    Reddit comment. Return "True"
    if the comment provides an opinion or sentiment 
    (either positive or negative) about {keyword}.
    If the comment does not include the {keyword}, or
    does not imply an opinion about {keyword} return
    "False". Be strict with your decisions to make sure
    the "True" comments are opinionated.
    """

    for post in post_list:
        prompt = prompt_prefix + post["comment"]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": f"You will read comments from Reddit users and filter out all comments that do not express any sentiment about {keyword}."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        opinionated_comment = response.choices[0].message.content.lower()
        if opinionated_comment == "true":
            # cleaned_comment = ' '.join(comment.splitlines()).strip()
            filtered_comments.append(post)

    return filtered_comments