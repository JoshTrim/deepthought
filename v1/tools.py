# Import things that are needed generically
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b



def search_function(query: str):
    return "LangChain"


search = StructuredTool.from_function(
    func=search_function,
    name="Search",
    description="useful for when you need to answer questions about current events",
    # coroutine= ... <- you can specify an async method if desired as well
)
