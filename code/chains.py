import ast
import datetime
import os
from typing import Dict

import dotenv
from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from prompting_tools import GCMDKeywordSearchTool, geocode
from prompts import (cmr_summarization_template, datetime_location_template,
                     datetime_template, multi_evidence_template,
                     multiple_context_qa_template, single_context_qa_template,
                     summarization_template)


class DatetimeChain(LLMChain):
    """Find datetime for a given time string"""

    def __init__(self, *args, **kwargs):
        today = datetime.date.today()
        today_string = (
            f"Assume the current year and month is {today.year} and {today.month}."
        )
        template = datetime_template.strip() + today_string
        prompt = PromptTemplate(
            template=template,
            input_variables=["datetime"],
        )
        super().__init__(prompt=prompt, llm=OpenAI(temperature=0), *args, **kwargs)

    def _run(self, timestring: str) -> str:
        """Find datetime for a given time string"""
        return self.predict(datetime=timestring)

    async def _arun(self, timestring: str) -> str:
        """asynchronous call to find datetime for a given time string"""
        return self.predict(datetime=timestring)


class DatetimeLocationFinderChain(LLMChain):
    """Find datetime for a given time string"""

    def __init__(self, *args, **kwargs):
        prompt = PromptTemplate(
            template=datetime_location_template.strip(),
            input_variables=["text"],
        )
        super().__init__(prompt=prompt, llm=OpenAI(temperature=0), *args, **kwargs)

    def _run(self, timestring: str) -> str:
        """Find datetime for a given time string"""
        return self.predict(datetime=timestring)

    async def _arun(self, timestring: str) -> str:
        """asynchronous call to find datetime for a given time string"""
        return self.predict(datetime=timestring)


class QASummarizeChain(LLMChain):
    """Summarize a given text, using a question answering format and answer the question"""

    def __init__(self, *args, **kwargs):
        prompt = PromptTemplate(
            template=summarization_template,
            input_variables=["query", "contexts"],
        )
        super().__init__(
            prompt=prompt,
            llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
            *args,
            **kwargs,
        )

    def _run(self, inputs: Dict) -> str:
        """Summarize a given text"""
        return self.predict(
            query=inputs["query"], context="\n".join(inputs["contexts"])
        )

    async def _arun(self, inputs: Dict) -> str:
        """asynchronous call to Summarize a given text"""
        return self.predict(
            query=inputs["query"], context="\n".join(inputs["contexts"])
        )
    
class CombinedQAChain(LLMChain):
    """Summarize a given text, using a question answering format and answer the question"""

    def __init__(self, *args, **kwargs):
        prompt = PromptTemplate(
            template=multiple_context_qa_template,
            input_variables=["query", "contexts"],
        )
        super().__init__(
            prompt=prompt,
            llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7),
            *args,
            **kwargs,
        )

    def _run(self, inputs: Dict) -> str:
        """Summarize a given text"""
        return self.predict(
            query=inputs["query"], context="\n".join(inputs["contexts"])
        )

    async def _arun(self, inputs: Dict) -> str:
        """asynchronous call to Summarize a given text"""
        return self.predict(
            query=inputs["query"], context="\n".join(inputs["contexts"])
        )


class SingleQAChain(LLMChain):
    """question answering chain to answer the question based on a given context"""

    def __init__(self, *args, **kwargs):
        prompt = PromptTemplate(
            template=single_context_qa_template,
            input_variables=["query", "context"],
        )
        if "model_name" in kwargs:
            if kwargs["model_name"] == "gpt-3.5-turbo":
                super().__init__(
                    prompt=prompt,
                    llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
                )
            else:
                super().__init__(
                    prompt=prompt,
                    llm=OpenAI(model_name=kwargs["model_name"], temperature=0.7),
                )
        else:
            super().__init__(
                prompt=prompt,
                llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
            )
        
         
    def _run(self, inputs: Dict) -> str:
        """Summarize a given text"""
        return self.predict(query=inputs["query"], context=inputs["context"])

    async def _arun(self, inputs: Dict) -> str:
        """asynchronous call to Summarize a given text"""
        return self.predict(query=inputs["query"], context=inputs["context"])


class CMRSummarizeChain(LLMChain):
    """Summarize a given structured CMR query result, using a question answering format and answer the question"""

    def __init__(self, *args, **kwargs):
        prompt = PromptTemplate(
            template=cmr_summarization_template,
            input_variables=["query", "cmr_responses"],
        )
        super().__init__(
            prompt=prompt,
            llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
            *args,
            **kwargs,
        )

    def _run(self, inputs: Dict) -> str:
        """Summarize a given text"""

        return self.predict(
            query=inputs["query"], context="\n".join(inputs["cmr_responses"])
        )

    async def _arun(self, inputs: Dict) -> str:
        """asynchronous call to Summarize a given text"""
        return self.predict(
            query=inputs["query"], context="\n".join(inputs["cmr_responses"])
        )

class EvidenceSelectorChain(LLMChain):
    """select the most accurate evidence from a list of evidences, based on the question"""

    def __init__(self, *args, **kwargs):
        prompt = PromptTemplate(
            template=multi_evidence_template,
            input_variables=["query", "evidences"],
        )
        super().__init__(
            prompt=prompt,
            llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
            *args,
            **kwargs,
        )

    def _run(self, inputs: Dict) -> str:
        """Summarize a given text"""
        assert isinstance(inputs["evidences"]) == list
        return self.predict(
            query=inputs["query"], context="\n\n".join(inputs["evidences"])
        )

    async def _arun(self, inputs: Dict) -> str:
        """asynchronous call to Summarize a given text"""
        assert isinstance(inputs["evidences"]) == list
        return self.predict(
            query=inputs["query"], context="\n\n".join(inputs["evidences"])
        )
