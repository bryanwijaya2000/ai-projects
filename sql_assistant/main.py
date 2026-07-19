from typing import Annotated
from typing_extensions import TypedDict, Optional
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
import mysql.connector
import gradio as gr

class SqlState(TypedDict):
    task: str
    messages: Annotated[list, add_messages]
    query: Optional[str]
    error: Optional[str]

def sql_list_tables() -> str:
    res = ""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{DB_NAME}'")
        result = cursor.fetchall()
        res = ", ".join([row[0] for row in result])
    except Exception as e:
        res = f"Error: {str(e)}"
    finally:
        conn.close()
    return res

def sql_table_schema(table_name: str) -> str:
    res = ""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute(f"SELECT column_name, data_type, column_comment FROM information_schema.columns WHERE table_schema = '{DB_NAME}' AND table_name = '{table_name}'")
        result = cursor.fetchall()
        res = "\n".join(f"{row[0]} ({row[1]}): {row[2]}" for row in result)
    except Exception as e:
        res = f"Error: {str(e)}"
    finally:
        conn.close()
    return res

def sql_db_schema() -> str:
    res = ""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute(f"SELECT table_name, table_comment FROM information_schema.tables WHERE table_schema = '{DB_NAME}'")
        result = cursor.fetchall()
        res = "\n\n".join([f"{row[0]}: {row[1]}\n{sql_table_schema(row[0])}" for row in result])
    except Exception as e:
        res = f"Error: {str(e)}"
    finally:
        conn.close()
    return res

def sql_db_relationships() -> str:
    res = ""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT
                table_name AS Parent_Table,
                column_name AS Parent_Column,
                referenced_table_name AS Referenced_Table,
                referenced_column_name AS Referenced_Column
            FROM information_schema.key_column_usage
            WHERE table_schema = '{DB_NAME}' 
            AND referenced_table_name IS NOT NULL
            """
        )
        result = cursor.fetchall()
        res = "\n".join([f"{row[0]}: {row[1]} - {row[2]}: {row[3]}" for row in result])
    except Exception as e:
        res = f"Error: {str(e)}"
    finally:
        conn.close()
    return res

def generate_query(state: SqlState) -> dict:
    task = state.get("task", "")
    messages = state.get("messages", [])
    query = state.get("query", "")
    error = state.get("error", "")

    if not error:
        prompt = ChatPromptTemplate.from_messages([
            ("user", "{task}")
        ])
        formatted_messages = prompt.format_messages(task=task)
    else:
        prompt = ChatPromptTemplate.from_messages([
            (
                "user",
                "The previous query throws an error. Please fix it accordingly.\n\n"
                "Task: {task}\n\n"
                "Previous query: {query}\n\n"
                "Error: {error}\n\n"
                "Provide only the fixed query."
            )
        ])
        formatted_messages = prompt.format_messages(task=task, query=query, error=error)
    
    inputs = messages + formatted_messages
    response = llm.invoke(inputs)

    return {
        "messages": [response],
        "query": response.content
    }

def check_query(state: SqlState) -> dict:
    query = state.get("query", "")
    res = {"error": ""}
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute(query)
    except Exception as e:
        res["error"] = str(e)
    finally:
        conn.close()
    return res
    
def should_fix_query(state: SqlState):
    if state["error"]:
        return "generate_query"
    return END

def get_query(task: str) -> str:
    result = sql_agent.invoke({
        "task": task,
        "messages": [("system", SYSTEM_MESSAGE)],
        "query": "",
        "error": ""
    })
    return result["query"]

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "sql_assistant_db"

SYSTEM_MESSAGE = f"""
    You are an expert SQL developer. Output ONLY valid, raw executable query.\n
    DO NOT do any of the following:\n
    - Include any markdown code blocks, backticks (```), or introductory/explanatory text\n
    - Output any other query types (INSERT, UPDATE, DELETE, or DDL) besides SELECT queries\n
    Below are the details of the database:\n\n
    Database name: {DB_NAME}\n\n
    Table names: {sql_list_tables()}\n\n
    Table schemas:\n\n
    {sql_db_schema()}\n\n
    Table relationships:\n\n
    {sql_db_relationships()}
"""

llm = ChatOllama(model="qwen3", temperature=0)

workflow = StateGraph(SqlState)

workflow.add_node("generate_query", generate_query)
workflow.add_node("check_query", check_query)

workflow.add_edge(START, "generate_query")
workflow.add_edge("generate_query", "check_query")
workflow.add_conditional_edges(
    "check_query",
    should_fix_query,
    {
        "generate_query": "generate_query",
        END: END
    }
)

sql_agent = workflow.compile()

interface = gr.Interface(
    inputs=gr.Textbox(
        lines=2,
        placeholder="Enter your SQL task here"
    ),
    outputs=gr.TextArea(),
    title="SQL Assistant",
    description="Enter your SQL task, and I will generate the query for you!",
    fn=get_query
)

interface.launch(debug=True)