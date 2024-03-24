# flake8: noqa
from langchain.prompts import BaseChatPromptTemplate
from langchain.prompts.prompt import PromptTemplate

# Set up the base template

single_context_qa_template = """
You are given a query and a context paragraph.
Answer the question. answers must be inferred based on the context paragraph only. Do not use any other information.
you must also provide the evidence sentence from the context paragraph that is used for inference.
Here is the context paragraph:
{context}
Provide Answer and Reference in following format
Answer: 
Evidence: 

(if there is no related information in the context paragraph that answers the question, you must output "N/A" in the Answer field and "N/A" in the Evidence field)
Here is the query: {query}
"""

multiple_context_qa_template = """
You are a truthful question answering bot. You are given a query and some context paragraphs.
Answer the question. answers must be grounded only on the context paragraphs. Do not use any other information.
you must also provide the evidence verbatim as it appears in the context paragraph. Do not include any other characters.
Here are the context paragraphs:
{contexts}
if there is no related information in the context paragraph that answers the question, you must output "N/A" in the Answer field and "N/A" in the Evidence field
Provide Answer and Evidence in following format
Answer: 
Evidence: 

Here is the query: {query}
"""


multi_evidence_template = """
You are a evidence selection bot. You are given a list of evidences, You must choose the most accurate evidence that answers the question.
Here is the list of evidences:
{evidences}
Here is the question: {query}
Most Accurate Evidence:
"""

summarization_template = """
You are a truthful question answer system. You are given a question and you must answer it based on the context paragraphs provided. 
You must also summarize the context paragraphs into a single paragraph.
you must also provide a reference to the source of the answer, which is the exact sencence from the context paragraph that answers the question.
If the question cannot be answered by the context provided, you must output "Cannot answer the question with the context paragraphs" in the Answer field.

Here are the context paragraphs:
{contexts}

Here is the question: {query}
Helpful Summary, followed by Answer, finally Reference:
"""
cmr_summarization_template = """
You are a Summarization system. You are given a query and some structured metadata related to query. 
You must summarize the structured metadata into a single paragraph, as it relates to the query.

Here are the CMR query results: 
{cmr_responses}

Here is the initial question: {query}
Helpful Summary:
"""
datetime_location_template = """
            You will be given a text. extract the time string and location string.
            the output SHOULD be in this format '(timestring, location string)'

            if either of the strings are empty, then return `None` in their place.

            text: {text}
            output:
            """

datetime_template = """
            convert time string: {datetime} into start and end datetime formatted as: 'temporal[]=yyyy-MM-ddTHH:mm:ssZ,yyyy-MM-ddTHH:mm:ssZ'
            """

cmr_template = """
Decode the following query as best you can.
The query will involve extracting datetime, bounding box and GKR science keyword. 
You have access to the following tools:

{tools}

Use the following format:

Query: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now have all the information for CMR query
Action: cmr_query_api
Action Input: the input to cmr_query_api (This is your last action, do not add any more actions, DO NOT include Base URL)
Observation: the result of the action
Final Answer: aggregate and Summarize the observation

Begin Loop:

Query: {input}
{agent_scratchpad}"""  # noqa: E501


bbox_time_kw_template = """\
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

The questions will involve getting datasets from a database.

To resolve the question, you have the following tools available that you can use.

Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

geocode:
e.g. geocode: Paris
Returns a bounding box for the location

gcmd_keyword:
e.g. gcmd_keyword: aerosol
Returns a list of GCMD keywords that match the input

cmr_search:
e.g. bbox: [-73.21, 43.99, -73.12, 44.05] && datetime=['2019-01-01T00:00:00Z', '2019-01-02T00:00:00Z'] && keyword: aerosol
Will search the database for that bbox, datetime and the science or data keyword present in the Question and return a JSON representation of the item assets returned from the CMR API. DON'T REPLACE the words bbox, datetime or keyword

Please remember that these are your only three available actions. Do not attempt to put any word after "Action: " other than calculate, geocode or cmr_search. THIS IS A HARD RULE. DO NOT BREAK IT AT ANY COST. DO NOT MAKE UP YOUR OWN ACTIONS.

Example session:

Question: Can you point me to aerosol data for 2019 January, for the capital of France?

Thought: I should deduce that capital of France is Paris, and find its bounding box extent.
Action: geocode: Paris
PAUSE

You will be called again with this:

Observation: Its bbox is [27, 54, 63, 32.5]


You then output:

Thought: I should now query the CMR catalog to fetch data about satellite images of Paris.

Action: cmr_search: bbox=[27, 54, 63, 32.5] && datetime=['2019-01-01T00:00:00Z', '2019-01-02T00:00:00Z'] && keyword: aerosol
PAUSE

You will be called again with the output from the CMR API as JSON. Use that to give the user concise and verbose information on the returned data. Stop generating after this.

"""  # noqa: C0103
bbox_time_kw_template = bbox_time_kw_template.strip()
