from typing import Annotated
from typing_extensions import TypedDict
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools import TavilySearchResults
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
import gradio as gr
import arxiv

# State class
class ResearchState(TypedDict):
    topic: str
    messages: Annotated[list, add_messages]
    draft: str
    critique: str
    revision_count: int
    tool_calls_count: int

# Nodes

def generate_report(state: ResearchState) -> dict:
    topic = state["topic"]
    messages = state.get("messages", [])
    draft = state.get("draft", "")
    critique = state.get("critique", "")
    revision_count = state.get("revision_count", 0)
    tool_calls_count = state.get("tool_calls_count", 0)

    system_message = (
        "You are an expert researcher. You have access to tools to find academic papers and web results. "
        "CRITICAL: If you do not have enough data yet, use your tools first to query facts before writing the final text report."
    )

    if not draft:
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("user", "You are a researcher. Write a research report about {topic}")
        ])
        formatted_messages = prompt.format_messages(topic=topic)
    else:
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            (
                "user",
                "Revise the previous draft base on the critique.\n\n"
                "Topic: {topic}\n\n"
                "Previous draft: {draft}\n\n"
                "Critique: {critique}\n\n"
                "Provide only the revised report."
            )
        ])
        formatted_messages = prompt.format_messages(topic=topic, draft=draft, critique=critique)

    inputs = messages + formatted_messages
    response = llm_with_tools.invoke(inputs)

    final_state = {
        "messages": [response]
    }

    new_calls_count = len(response.tool_calls) if response.tool_calls else 0

    if not response.tool_calls or tool_calls_count + new_calls_count >= 2:
        final_state["draft"] = response.content
        final_state["revision_count"] = revision_count + 1
    else:
        final_state["tool_calls_count"] = tool_calls_count + new_calls_count

    return final_state

def critique_report(state: ResearchState) -> dict:
    prompt = ChatPromptTemplate.from_template(
        "You a an expert academic peer-reviewer.\n"
        "Analyze and review the following research report for improvements.\n\n"
        "Report:\n\n{draft}\n\n"
        "In case the report is already good enough and does not require any improvements, respond with: 'APPROVED'."
    )
    response = llm.invoke(prompt.format(draft=state["draft"]))
    return {
        "critique": response.content
    }

# Conditional routings

def route_generator(state: ResearchState) -> str:
    last_message = state["messages"][-1]
    if last_message.tool_calls and state.get("tool_calls_count", 0) < 2:
        return "tools"
    return "critique"

def route_critique(state: ResearchState):
    if "APPROVED" in state["critique"].upper() or state.get("revision_count", 0) >= 3:
        return END
    return "generate"

# Tools

@tool
def web_search(topic: str) -> str:
    """
    Searches the web for the given topic
    Args:
        topic: The input topic to search for
    Returns:
        str: Search results
    """
    results = TavilySearchResults(max_results=5).invoke(topic)
    return str(results)

@tool
def call_api(topic: str) -> str:
    """
    Calls an API to find research papers relevant to the given topic
    Args:
        topic: The input topic or topic
    Returns:
        str: Summary of findings
    """
    client = arxiv.Client()

    search = arxiv.Search(
        query=topic,
        max_results=5,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    summary = []

    for paper in client.results(search):
        summary.append(f"Title: {paper.title}\nSummary: {paper.summary}\n")
    
    return "\n".join(summary) if summary else "No papers found."

# Get final report
def get_report(topic: str) -> str:
    result = research_agent.invoke({
        "topic": topic,
        "messages": [],
        "draft": "",
        "critique": "",
        "revision_count": 0,
        "tool_calls_count": 0
    })
    return result["draft"]

tools = [web_search, call_api]
tool_node = ToolNode(tools)

llm = ChatOllama(model="qwen3", temperature=0)
llm_with_tools = llm.bind_tools(tools)

# Graph State
workflow = StateGraph(ResearchState)

# Nodes
workflow.add_node("generate", generate_report)
workflow.add_node("tools", tool_node)
workflow.add_node("critique", critique_report)

# Edges
workflow.add_edge(START, "generate")
workflow.add_conditional_edges(
    "generate",
    route_generator,
    {
        "tools": "tools",
        "critique": "critique"
    }
)
workflow.add_edge("tools", "generate")
workflow.add_conditional_edges(
    "critique",
    route_critique,
    {
        "generate": "generate",
        END: END
    }
)

# Compile the built graph
research_agent = workflow.compile()

interface = gr.Interface(
    inputs=gr.Textbox(
        lines=2,
        placeholder="Enter your research topic here (e.g. Black holes)"
    ),
    outputs=gr.TextArea(),
    title="Research Assistant",
    description="Enter your research topic, and I will write the report for you!",
    fn=get_report
)

interface.launch(debug=True)