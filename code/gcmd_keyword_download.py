import os
import re
from typing import List

import dotenv
import fastapi
import httpx
import requests
import xmltodict
from gpt_embedder import GPTEmbedder

dotenv.load_dotenv()

KEYWORD_URL = "https://gcmd.earthdata.nasa.gov/kms/tree/concept_scheme/all?version=15.9"


def get_keyword_tree():
    """Get the keyword tree from the GCMD API"""
    response = requests.get(KEYWORD_URL)
    response.raise_for_status()

    keyword_tree = response.json()["tree"]["treeData"][0]
    # assert keyword_tree.keys() == dict_keys(['key', 'title', 'children'])
    # title contains path name
    paths_list = []
    recurse_get_paths(keyword_tree, path="", paths_list=paths_list)
    return [path.strip(" > Keywords > ") for path in paths_list]


def recurse_get_paths(keyword_tree, path="", paths_list=[]):
    """Recursively get paths from the keyword tree"""
    if keyword_tree["children"]:
        for child in keyword_tree["children"]:
            recurse_get_paths(
                child, path=path + " > " + keyword_tree["title"], paths_list=paths_list
            )
    else:
        paths_list.append(path + " > " + keyword_tree["title"])


def expand_keywords(paths_list):
    """Expand keywords to include parent keywords in the leaf node"""
    expanded_paths_list = []
    for path in paths_list:
        path_list = path.split(" > ")
        for i, _ in enumerate(path_list):
            expanded_paths_list.append(" > ".join(path_list[: i + 1]))
        expanded_paths_list
    return expanded_paths_list


def filter_paths(paths_list, top_level_keywords: List[str]):
    """Filter paths to only include those that contain the top level keyword"""
    return [path for path in paths_list if any(kw in path for kw in top_level_keywords)]


if __name__ == "__main__":
    import ipdb

    ipdb.set_trace()
    keys = expand_keywords(
        filter_paths(get_keyword_tree(), ["Earth Science", "Earth Science Services"])
    )
