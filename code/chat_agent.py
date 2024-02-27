### deprecated code, only for reference
import os
import re

import dotenv
import httpx
import openai
from cmr import CollectionQuery, GranuleQuery

collection_query = CollectionQuery()
granule_query = GranuleQuery()
action_re = re.compile("^Action: (\w+): (.*)$")


### this is chat agent using react, without the use of Langchain
class ChatBot:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})

    async def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = await self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    async def execute(self):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=self.messages
        )
        # Uncomment this to print out token usage each time, e.g.
        # {"completion_tokens": 86, "prompt_tokens": 26, "total_tokens": 112}
        print(completion.usage)
        return completion.choices[0].message.content


async def get_keyword(self, keyword, gpt_embedder):
    """Get the nearest keyword to the given keyword"""
    return gpt_embedder.find_nearest_kw(keyword)


async def cmr_collection_search(action_input):
    """Search CMR using the CMR rest API"""
    CMR_SEARCH_URL = "https://cmr.earthdata.nasa.gov/search/collections"
    async with httpx.AsyncClient() as client:
        response = await client.get(CMR_SEARCH_URL, params={"keyword": action_input})
        return response.json()


async def cmr_search_py(action_input):
    # example action_input "bbox=[2.224122, 48.8155755, 2.4697602, 48.902156] && datetime=['2019-01-01T00:00:00Z', '2019-01-31T23:59:59Z'] && keyword: aerosol"
    # TODO: extract bbox, datetime, keyword in format:
    # keyword = aerosol,
    # bbox=[-180, -90, 180, 90],
    # start_date="2000-01-01T00:00:00Z",
    # end_date="2021-01-01T00:00:00Z",
    keyword = re.search("keyword: (.*)", action_input).group(1)
    bbox_match = re.search(r"bbox=\[(.*?)\]", action_input)
    datetime_match = re.search(r"datetime=\[(.*?)\]", action_input)

    # Check if bbox and datetime arrays are found
    if bbox_match and datetime_match:
        bbox_str = bbox_match.group(1)
        datetime_str = datetime_match.group(1)
        bbox = [float(x) for x in bbox_str.split(",")]
        datetime = [x for x in datetime_str.split(",")]
        start_date = datetime[0].replace("'", "").strip()
        end_date = datetime[1].replace("'", "").strip()
        print("bbox:", bbox)
        print("start_date:", start_date)
        print("end_date:", end_date)
        print("keyword:", keyword)
    result = (
        collection_query.keyword(keyword)
        .bounding_box(*bbox)
        .temporal(start_date, end_date)
    ).get(1)[0]
    # filter by keys if they exist:
    filter_keys = [
        "title",
        "archive center",
        "time_start",
        "updated",
        "links",
    ]
    filtered_result = {
        result_key: result[result_key]
        for result_key in result.keys()
        if result_key in filter_keys
    }

    return filtered_result


async def query(question, max_turns=5):
    i = 0
    bot = ChatBot(bbox_time_kw_template)
    next_prompt = question
    while i < max_turns:
        i += 1
        result = await bot(next_prompt)
        print(result)
        actions = [action_re.match(a) for a in result.split("\n") if action_re.match(a)]
        if actions:
            # There is an action to run
            action, action_input = actions[0].groups()
            if action not in known_actions:
                raise Exception("Unknown action: {}: {}".format(action, action_input))
            print(" -- running {} {}".format(action, action_input))
            observation = await known_actions[action](action_input)
            print("Observation:", observation)

            # If the action is querying the CMR API, just return the results, don't re-prompt

            next_prompt = "Observation: {}".format(observation)
        else:
            return result


known_actions = {
    "cmr_search": cmr_search_py,
    "calculate": calculate,
    "geocode": geocode,
}
}
