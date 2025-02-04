from openai import OpenAI
import os
from dotenv import load_dotenv
import pprint


load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def filter_comments(comment_list, keyword):
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

    for comment in comment_list:
        prompt = prompt_prefix + comment
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
            filtered_comments.append(comment)

    return filtered_comments


# def filter_comments(comment_list, keyword):
#     formatted_comments = "\n".join([f"{i+1}: {comment}" for i, comment in enumerate(comment_list)])

#     filtered_comments = []

#     prompt = f"""The following is a list of
#     Reddit comments. Return a list containing only
#     the comments that provide a sentiment 
#     (positive, negative, or neutral) on {keyword}.\n"""

#     prompt += formatted_comments

#     print(prompt)

#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         temperature=0,
#         messages=[
#             {
#                 "role": "system",
#                 "content": f"You will read comments from Reddit users and filter out all comments that do not express any sentiment about {keyword}."
#             },
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ]
#     )

#     filtered_comments = response['choices'][0]['message']['content'].strip()
#     filtered_comments_list = filtered_comments.split('\n')

#     print(filtered_comments_list)