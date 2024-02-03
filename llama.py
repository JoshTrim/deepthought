from langchain_community.llms import Ollama

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# Basic streaming query
# llm = Ollama(model="llama2")
#
# query = "Tell me a joke"
#
# for chunks in llm.stream(query):
#     print(chunks, sep=' ', end='')


# Tool example
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
tool = WikipediaQueryRun(api_wrapper=api_wrapper)
