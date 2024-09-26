import os
from llama_index.core import Settings
from support.redis_service import RedisService
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from support.top_k_retriever import TopKRetriever

from llama_index.core.schema import QueryBundle
from llama_index.core.response.notebook_utils import display_source_node


class SimpleRagQueryEngine():
    def __init__(self, documents: list):
        self.documents = documents

    def buildQueryEngine(self):
        redis_store = RedisService(index_name=os.getenv('TOOL_NAME'), dimensions=1024, overwrite=True).createVectorStore()

        # Create storage context and index
        storage_context = StorageContext.from_defaults(vector_store=redis_store)
        vector_store = VectorStoreIndex.from_documents(documents=self.documents, storage_context=storage_context)

        retriever = VectorIndexRetriever(index=vector_store, similarity_top_k=4)

        query_engine = RetrieverQueryEngine(
            retriever=retriever,
            node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7,
                                                         filter_empty=True,
                                                         filter_duplicates=True,
                                                         filter_similar=False, ), ]
        )

        comparison = TopKRetriever([1, 2, 3, 4, 5], vector_store,'What are the responsibilities of the Manager Software Engingeering?').compare()

        return query_engine


from llama_index.core.query_pipeline import QueryPipeline as QP

qp = QP(verbose=True)
from llama_index.core.agent.react.types import (
    ActionReasoningStep,
    ObservationReasoningStep,
    ResponseReasoningStep,
)
from llama_index.core.agent import Task, AgentChatResponse
from llama_index.core.query_pipeline import (
    AgentInputComponent,
    AgentFnComponent,
    CustomAgentComponent,
    QueryComponent,
    ToolRunnerComponent,
)
from llama_index.core.llms import MessageRole
from typing import Dict, Any, Optional, Tuple, List, cast


## Agent Input Component
## This is the component that produces agent inputs to the rest of the components
## Can also put initialization logic here.
def agent_input_fn(task: Task, state: Dict[str, Any]) -> Dict[str, Any]:
    """Agent input function.
Returns:
        A Dictionary of output keys and values. If you are specifying
        src_key when defining links between this component and other
        components, make sure the src_key matches the specified output_key.
"""
    # initialize current_reasoning
    if "current_reasoning" not in state:
        state["current_reasoning"] = []
    reasoning_step = ObservationReasoningStep(observation=task.input)
    state["current_reasoning"].append(reasoning_step)
    return {"input": task.input}


agent_input_component = AgentInputComponent(fn=agent_input_fn)

from llama_index.core.agent import ReActChatFormatter
from llama_index.core.query_pipeline import InputComponent, Link
from llama_index.core.llms import ChatMessage
from llama_index.core.tools import BaseTool

system_header_new = '''You are trying to generate a proper natural language response given a user input query.This 
query will be used as input for the topKcandidates tool agent.\n\n## Tools\n\n You are responsible for using this 
tool to complete the task at hand.\nThis may require breaking the task into subtasks and using this tool to complete 
each subtask.\n\nYou have access to the  tool:\n{tool_desc}\n\n\n## Output Format\n\nPlease answer in the same 
language as the question and use the following format:\n\n```\nThought: The current language of the user is: (user\'s 
language). I need to use the tool to help me answer the question.\nAction: tool name (one of {tool_names}) if using a 
tool.\nAction Input: the input to the tool, in a JSON format representing the kwargs (e.g. {{"input": "hello world", 
"num_beams": 5}})\n```\n\nPlease ALWAYS start with a Thought.\n\nPlease use a valid JSON format for the Action Input. 
Do NOT do this {{\'input\': \'hello world\', \'num_beams\': 5}}.\n\nIf this format is used, the user will respond in 
the following format:\n\n```\nObservation: tool response\n```\n\nYou should keep repeating the above format and 
increasing the top_k (starting from top_k=1) till you have enough information to answer the question without using 
tool again. At that point, you MUST respond in the one of the following two formats:\n\n```\nThought: I can answer 
without using the tool again. I\'ll use the user\'s language to answer\nAnswer: [your answer here (In the same 
language as the user\'s question)]\n```\n\n```\nThought: I cannot answer the question with the provided 
tool.\nAnswer: [your answer here (In the same language as the user\'s question)]\n```\n\n## Current 
Conversation\n\nBelow is the current conversation consisting of interleaving human and assistant messages.\n'''

system_headerOriginal = '''You are designed to help with a variety of tasks, from answering questions to providing 
summaries to other types of analyses.\n\n## Tools\n\nYou have access to a wide variety of tools. You are responsible 
for using the tools in any sequence you deem appropriate to complete the task at hand.\nThis may require breaking the 
task into subtasks and using different tools to complete each subtask.\n\nYou have access to the following tools:\n{
tool_desc}\n\n\n## Output Format\n\nPlease answer in the same language as the question and use the following 
format:\n\n```\nThought: The current language of the user is: (user\'s language). I need to use a tool to help me 
answer the question.\nAction: tool name (one of {tool_names}) if using a tool.\nAction Input: the input to the tool, 
in a JSON format representing the kwargs (e.g. {{"input": "hello world", "num_beams": 5}})\n```\n\nPlease ALWAYS 
start with a Thought.\n\nPlease use a valid JSON format for the Action Input. Do NOT do this {{\'input\': \'hello 
world\', \'num_beams\': 5}}.\n\nIf this format is used, the user will respond in the following 
format:\n\n```\nObservation: tool response\n```\n\nYou should keep repeating the above format till you have enough 
information to answer the question without using any more tools. At that point, you MUST respond in the one of the 
following two formats:\n\n```\nThought: I can answer without using any more tools. I\'ll use the user\'s language to 
answer\nAnswer: [your answer here (In the same language as the user\'s question)]\n```\n\n```\nThought: I cannot 
answer the question with the provided tools.\nAnswer: [your answer here (In the same language as the user\'s 
question)]\n```\n\n## Current Conversation\n\nBelow is the current conversation consisting of interleaving human and 
assistant messages.\n'''


## define prompt function
def react_prompt_fn(
        task: Task, state: Dict[str, Any], input: str, tools: List[BaseTool]
) -> List[ChatMessage]:
    # Add input to reasoning
    chat_formatter = ReActChatFormatter(system_header=system_header_new)

    return chat_formatter.format(
        tools,
        chat_history=task.memory.get() + state["memory"].get_all(),
        current_reasoning=state["current_reasoning"],
    )


react_prompt_component = AgentFnComponent(
    fn=react_prompt_fn, partial_dict={"tools": [topK_tool]}
)
