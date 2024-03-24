import json
import os

import dotenv
import numpy as np
import openai
import utils
from langchain.embeddings import OpenAIEmbeddings

dotenv.load_dotenv()


class GPTEmbedder:
    """Embedder for keywords using GPT-3 embeddings"""

    def __init__(
        self,
        embeddings_file="/Users/mramasub/work/cmr-prompt-chain/data/keyword_embeddings.npy",
    ):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.embedder = OpenAIEmbeddings(openai_api_key=openai.api_key)
        self.text_to_add = "Hierarchy Path: "
        # print pwd
        print(os.getcwd())
        keywords_file = "/Users/mramasub/work/cmr-prompt-chain/data/keywords.json"
        if utils.path_exists(keywords_file):
            self.kws = self.read_kws(keywords_file)
        else:
            # exit
            pass
        self.model = "text-embedding-ada-002"
        self.embeddings = (
            self.load_from_pkl(embeddings_file)
            if utils.path_exists(embeddings_file)
            else self.create_embeddings()
        )

        assert len(self.kws) == len(self.embeddings)

    def create_embeddings(self):
        """Create embeddings for all keywords"""
        kws_to_embed = self.kws
        embeddings = self._embed_langchain(kws_to_embed)
        return np.array(embeddings)

    def _embed_langchain(self, texts, use_text_to_add=True):
        text_to_add = ""
        if use_text_to_add:
            text_to_add = self.text_to_add
        return self.embedder.embed_documents([text_to_add + text for text in texts])

    def _embed(self, texts, use_text_to_add=True):
        text_to_add = ""
        if use_text_to_add:
            text_to_add = self.text_to_add
        return openai.Embedding.create(
            input=[text_to_add + kw for kw in texts], model=self.model
        )

    def find_nearest_kw(self, keyword, top_n=1):
        """Find the nearest keyword to the given keyword"""
        embedding = self._embed_langchain([keyword], use_text_to_add=False)
        embedding = np.array(embedding)
        distances = np.linalg.norm(self.embeddings - embedding, axis=1)

        return [self.kws[i] for i in np.argsort(distances)[:top_n]]

    def read_kws(
        self,
        file,
    ):
        """Read keywords from file"""
        kws = []

        with open(file, "r", encoding="utf-8") as f:
            kws = json.load(f)
        return [kw["keyword_string"] for kw in kws]

    def load_from_pkl(self, file):
        """Load embeddings from pickle file"""
        return np.load(file)
