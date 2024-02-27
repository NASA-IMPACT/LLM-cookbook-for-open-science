import os
import re

import dotenv
import httpx
import requests
import tiktoken
import xmltodict
from gpt_embedder import GPTEmbedder
from langchain.agents import Tool, tool
from langchain.tools import BaseTool
from opencage.geocoder import OpenCageGeocode

dotenv.load_dotenv()

gpt_embedder = GPTEmbedder(embeddings_file="../data/keyword_embeddings.npy")
opencage_geocoder = OpenCageGeocode(os.environ["OPENCAGE_API_KEY"])


class BoundingBoxFinderTool(BaseTool):
    name = "bounding_box_finder"
    description = "useful to find bounding box in min Longitude, min Latitude, max Longitude, max Latitude format for a given location, region, or a landmark. The output is formatted for CMR API."
    geocoder = opencage_geocoder

    def _run(self, tool_input: str) -> str:
        """Geocode a query (location, region, landmark)"""
        response = self.geocoder.geocode(tool_input, no_annotations="1")
        if response:
            bounds = response[0]["bounds"]
            # convert to bbox
            bbox = "{},{},{},{}".format(
                bounds["southwest"]["lng"],
                bounds["southwest"]["lat"],
                bounds["northeast"]["lng"],
                bounds["northeast"]["lat"],
            )
            return f"bounding_box[]={bbox}"
        return "Cannot parse the query"

    async def _arun(self, tool_input: str) -> str:
        """asynchronous call to Geocode a query"""
        async with httpx.AsyncClient() as client:
            response = self.geocoder.geocode(tool_input, no_annotations="1")
            if response:
                bounds = response[0]["bounds"]
                # convert to bbox
                # bounding_box[]=
                bbox = "{},{},{},{}".format(
                    bounds["southwest"]["lng"],
                    bounds["southwest"]["lat"],
                    bounds["northeast"]["lng"],
                    bounds["northeast"]["lat"],
                )
                return f"bounding_box[]={bbox}"

            else:
                return "Cannot parse the query"


def geocode(text: str) -> str:
    """Geocode a query (location, region, or landmark)"""
    response = opencage_geocoder.geocode(text, no_annotations="1")
    if response:
        bounds = response[0]["bounds"]
        # convert to bbox
        bbox = "{},{},{},{}".format(
            bounds["southwest"]["lng"],
            bounds["southwest"]["lat"],
            bounds["northeast"]["lng"],
            bounds["northeast"]["lat"],
        )
        return f"bounding_box[]={bbox}"

    @tool
    async def calculate(expression):
        """Calculate an expression"""
        return eval(expression)


class CMRQueryTool(BaseTool):
    name = "cmr_query_api"
    description = "useful for Querying CMR API based on previous Observations. input is query parameters string"
    base_url = "https://cmr.earthdata.nasa.gov/search/collections?"

    def _run(self, tool_input: str) -> str:
        k: int = 40
        """Filter a CMR response"""

        if self.base_url in tool_input:
            tool_input = tool_input.replace(self.base_url, "")
        # print(f"\nCMR Query URL{self.base_url + tool_input}\n")
        # response = requests.get(self.base_url + tool_input)
        # # parse xml response
        # xml_dict = xmltodict.parse(response.text)
        # hits = xml_dict["results"]["hits"]
        # k = int(hits) if int(hits) < k else k
        # if hits == "0":
        #     result_str = "No results found"
        # else:
        #     result_str = (
        #         f"Found {hits} results. here are top {k} result descriptions:\n"
        #     )
        #     if isinstance(xml_dict["results"]["references"]["reference"], list):
        #         for result in xml_dict["results"]["references"]["reference"]:
        #             result_str += f"{result['name']}\n"

        #     elif isinstance(xml_dict["results"]["references"]["reference"], dict):
        #         result_str += (
        #             f"{xml_dict['results']['references']['reference']['name']}\n"
        #         )
        return self.base_url + tool_input

    async def _arun(self, tool_input: str) -> str:
        """asynchronous call to filter a CMR response"""
        return [self._filter_response(tool_input)]


class GCMDKeywordSearchTool(BaseTool):
    """Search for science keyword in GCMD science keyword database. only earth science keywords are allowed, no other keywords are allowed"""

    # science_keywords\[0\]\[category\]=Cat1&science_keywords\[0\]\[topic\]=Topic1&science_keywords\[1\]\[category\]=Cat2

    name = "gcmd_keyword_search"
    description = "useful to search for earth science keyword in GCMD database. only earth science keywords and phenomena are allowed as inputs, no other keywords are allowed. The output is formatted for CMR API."

    def _run(self, tool_input: str, cmr_formatted=False) -> str:
        """Search for a keyword in GCMD"""
        if cmr_formatted:
            return self.get_formatted_science_kws(tool_input)
        else:
            return self.get_science_kws(tool_input)

    @staticmethod
    def get_formatted_science_kws(tool_input: str, top_n=5) -> str:
        """Search for a keyword in GCMD"""
        return [
            GCMDKeywordSearchTool().cmr_science_keyword(kw, keyword_pos)
            for keyword_pos, kw in enumerate(
                gpt_embedder.find_nearest_kw(tool_input, top_n=top_n)
            )
        ]

    @staticmethod
    def get_science_kws(tool_input: str, top_n=5) -> str:
        """Search for a keyword in GCMD"""
        return [kw for kw in gpt_embedder.find_nearest_kw(tool_input, top_n=top_n)]

    async def _arun(self, tool_input: str) -> str:
        """Search for a keyword in GCMD"""
        return [
            self.cmr_science_keyword(kw, keyword_pos)
            for keyword_pos, kw in enumerate(gpt_embedder.find_nearest_kw(tool_input))
        ][0]

    @staticmethod
    def cmr_science_keyword(keyword_string, keyword_pos):
        level_list = [
            "category",
            "topic",
            "term",
            "variable-level-1",
            "variable-level-2",
            "variable-level-3",
            "detailed-variable",
        ]
        keyword_list = [key.strip() for key in keyword_string.split(">")]

        return "&".join(
            [
                rf"science_keywords[{keyword_pos}][{level_list[i]}]={keyword_list[i].replace(' ', '%20')}"
                for i in range(len(keyword_list))
            ]
        )


def num_tokens_from_string(string: str, model_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


if __name__ == "__main__":
    text_src = "/Users/mramasub/work/BERT-E/cmr_records-chunks-300-10w_pdfminer.json"
    # read json
    import json

    with open(text_src, "r") as f:
        chunks = json.load(f)
    token_sizes = []
    for i, chunk in enumerate(chunks):
        token_sizes.append(num_tokens_from_string(chunk["text"], "gpt-3.5-turbo"))
        if i > 1000:
            print(f"Average number of tokens per chunk: {sum(token_sizes)/i}")
            break
