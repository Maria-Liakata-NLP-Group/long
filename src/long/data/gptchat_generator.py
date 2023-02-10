import os
import openai
from icecream import ic
from pathlib import Path
import random
import datetime
import math
import pandas as pd
from io import StringIO
import re
import time

# openai.api_key = os.getenv("OPENAI_API_KEY")

openai.api_key_path = Path.home() / ".openai-api-key"


"""
Topics that are deliberately benign or even asinine.
"""
TOPICS = [
    "the weather",
    "favourite pets and why",
    "nostalgia for childrens TV programmes",
]


def get_prompt(topic: str, number_of_msg: int, number_of_users: int) -> str:
    prompt = (
        f"Create the conversation between {number_of_users} users of a chat forum. The topic is {topic}. There should be {number_of_msg} distinct messages."
        """
    The results must a CSV file with the columns 'msg_id', 'username', 'text'. The 'text' column must be enclosed with double quotes.
    """
    )
    # [
    #     {
    #         "msg_id": 1,
    #         "username" :"user1",
    #         "text" : "It\\'s so cold outside!"
    #     },
    #     {
    #         "msg_id": 2
    #         "username": "user2"
    #         "text": "I heard it\\'s supposed to get even colder this week!"
    #     }
    # ]

    # The results must in the form of a python pandas DataFrame, with a schema matching in this example:

    # ```
    # chat_data = pd.DataFrame([
    #     [1, 'user1', 'It\\'s so cold outside!'],
    #     [2, 'user2', 'I heard it\\'s supposed to get even colder this week!'],
    #     ], columns=['msg_id', 'username', 'text'])
    # ```

    return prompt


def get_response(prompt):
    response = None
    attempts = 0

    while response is None:
        attempts += 1
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0.7,
                max_tokens=3500,
                top_p=1,
                frequency_penalty=0.5,
                presence_penalty=0.5,
            )
        except (
            openai.error.ServiceUnavailableError,
            openai.error.RateLimitError,
        ) as oia_error:
            if attempts > 50:
                raise oia_error
            time.sleep(30)

    return response


def get_sampling_threads(num_unique_threads: int):
    MAX_MSG_PER_THREAD = 40
    MODE_MSG_PER_THREAD = 5

    now_str = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    result_df = pd.DataFrame()

    for thread_id in range(num_unique_threads):

        the_topic = random.choice(TOPICS)
        number_of_msg = int(
            random.triangular(1, MAX_MSG_PER_THREAD, MODE_MSG_PER_THREAD)
        )

        min_users = 2 if number_of_msg > 2 else 1
        max_users = max(min_users, number_of_msg)
        number_of_users = (
            random.randrange(min_users, max_users)
            if max_users > min_users
            else min_users
        )

        ic(thread_id, the_topic, number_of_msg, number_of_users)

        the_prompt = get_prompt(the_topic, number_of_msg, number_of_users)
        # ic(the_prompt)

        next_df = None
        attempt = 0

        response = get_response(the_prompt)
        ic(response["choices"][0]["text"])

        next_df = pd.DataFrame(
            {
                "thread_id": thread_id,
                "number_of_msg": number_of_msg,
                "number_of_users": number_of_users,
                "raw_text": response["choices"][0]["text"],
            },
            index=[thread_id],
        )

        # while next_df is None and attempt < 5:
        #     attempt += 1
        #     ic(attempt)
        #     response = get_response(the_prompt)
        #     print(response["choices"][0]["text"])
        #     with open(f"openai_response_{thread_id}.txt", "w") as out_file:
        #         out_file.write(str(response))

        #     next_df = parse_response(response=response, thread_id=thread_id)

        if next_df is None:
            raise ValueError("Unable to get parable response from OpenAI")

        next_df.to_csv(f"openai_response_{thread_id}.csv")

        result_df = pd.concat([result_df, next_df])
        result_df.to_json(f"openai_output_{now_str}.json")
        # ic(response)

    return result_df


def combine_json_files():

    in_files = [
        "openai_output_20230118T184035.json",
        "openai_output_20230120T172705.json",
        "openai_output_20230123T175624.json",
    ]

    df = pd.DataFrame()

    for in_file in in_files:
        in_df = pd.read_json(in_file)

        df = pd.concat([df, in_df], ignore_index=True)
        df["thread_id"] = df.index
        df = df.head(300)
        df.to_json(f"openai_thread_pool.json")
        ic(len(in_df), len(df))


if __name__ == "__main__":

    # # ic(create_timestamps(6))
    # now_str = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    # ic(now_str)
    # result_df = get_sampling_threads(2)
    # ic(result_df.head(20))
    # result_df.to_json(f"openai_output_{now_str}.json")
    # # ic(response["choices"][0]["text"])

    combine_json_files()

    # with open("openai_output.txt", "w") as out_file:
    #     out_file.write(response["choices"][0]["text"])
    # result_df = pd.read_csv("openai_output.csv")
    # gbdf = result_df.groupby("thread_id")
    # ic(result_df.head())
    # ic(gbdf.count())
