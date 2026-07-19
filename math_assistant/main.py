from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
import gradio as gr

@tool
def web_search(query: str) -> str:
    """
    Searches the web for the given query
    Args:
        query: The input query to search for
    Returns:
        str: Search results
    """
    try:
        search_tool = TavilySearchResults(max_results=5)
        search_results = search_tool.invoke(query)
        return search_results
    except Exception as e:
        raise e

@tool
def add(a: float, b: float) -> float:
    """
    Adds two numbers
    Args:
        a: First number
        b: Second number
    Returns:
        float: The result
    """
    return a + b

@tool
def subtract(a: float, b: float) -> float:
    """
    Subtracts two numbers
    Args:
        a: First number
        b: Second number
    Returns:
        float: The result
    """
    return a - b

@tool
def multiply(a: float, b: float) -> float:
    """
    Multiplies two numbers
    Args:
        a: First number
        b: Second number
    Returns:
        float: The result
    """
    return a * b

@tool
def divide(a: float, b: float) -> float:
    """
    Divides two numbers
    Args:
        a: First number
        b: Second number
    Returns:
        float: The result
    """
    return a / b

def get_answer(query: str) -> str:
    response = agent_executor.invoke({"user_query": query})
    return response["output"]

llm = ChatOllama(model="qwen3", temperature=0)

tools = [web_search, add, subtract, multiply, divide]

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("placeholder", "{chat_history}"),
        ("human", "{user_query}"),
        ("placeholder", "{agent_scratchpad}")
    ]
)

agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

interface = gr.Interface(
    inputs=gr.Textbox(
        lines=2,
        placeholder="Enter your math problem here (e.g. Calculate 1+1.)"
    ),
    outputs=gr.TextArea(),
    title="Math Assistant",
    description="Enter your math problem, and I will solve it for you!",
    fn=get_answer
)

interface.launch(debug=True)