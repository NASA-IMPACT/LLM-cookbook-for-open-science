import re
from typing import List, Union

from chains import DatetimeChain
from langchain import LLMChain, OpenAI
from langchain.agents import (
    AgentExecutor,
    AgentOutputParser,
    LLMSingleActionAgent,
    Tool,
)
from langchain.chat_models import ChatOpenAI

# from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import BaseChatPromptTemplate
from langchain.schema import AgentAction, AgentFinish, HumanMessage
from prompting_tools import BoundingBoxFinderTool, CMRQueryTool, GCMDKeywordSearchTool
from prompts import cmr_template


class CustomPromptTemplate(BaseChatPromptTemplate):
    """
    This is a custom prompt template that uses the `cmr_template` from `prompts.py`
    """

    template: str
    tools: List[Tool]

    def format_messages(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        kwargs["agent_scratchpad"] = thoughts
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join(
            [f"{tool.name}: {tool.description}" for tool in self.tools]
        )
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        formatted = self.template.format(**kwargs)
        return [HumanMessage(content=formatted)]


class CustomOutputParser(AgentOutputParser):
    """
    This is a custom output parser that parses the output of the LLM agent
    """

    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
        # Parse out the action and action input
        regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(
            tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output
        )


class CMRQueryAgent:
    """
    This is a custom agent that uses the `CustomPromptTemplate` and `CustomOutputParser`
    """

    def __init__(self):
        self.create_tools()
        self.tool_names = [tool.name for tool in self.tools]
        self.prompt = CustomPromptTemplate(
            template=cmr_template,
            tools=self.tools,
            # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
            # This includes the `intermediate_steps` variable because that is needed
            input_variables=["input", "intermediate_steps"],
        )
        self.output_parser = CustomOutputParser()
        self.llm_chain = LLMChain(
            llm=ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0),
            prompt=self.prompt,
        )
        self.create_agent()

    def create_tools(self):
        """create tools for the agent"""
        self.tools = [
            Tool(
                name=BoundingBoxFinderTool().name,
                description=BoundingBoxFinderTool().description,
                func=BoundingBoxFinderTool().run,
            ),
            Tool(
                name="DateTime Extractor",
                description="Extracts time string and converts it to a datetime format",
                func=DatetimeChain().run,
            ),
            Tool(
                name=GCMDKeywordSearchTool().name,
                description=GCMDKeywordSearchTool().description,
                func=GCMDKeywordSearchTool().run,
            ),
            Tool(
                name=CMRQueryTool().name,
                description=CMRQueryTool().description,
                func=CMRQueryTool().run,
            ),
        ]

    def create_agent(self):
        self.agent = LLMSingleActionAgent(
            llm_chain=self.llm_chain,
            output_parser=self.output_parser,
            stop=["\nObservation:"],
            allowed_tools=self.tool_names,
        )
        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=self.agent, tools=self.tools, verbose=True
        )

    def run_query(self, input_text: str):
        return self.agent_executor.run(input_text)


if __name__ == "__main__":
    query_agent = CMRQueryAgent()
    query_agent.run("what is the time in new york?")
