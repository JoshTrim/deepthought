from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


llm = ChatOllama(model="llama2-uncensored")
prompt = ChatPromptTemplate.from_template("Tell me a short joke about {topic}")

# https://python.langchain.com/docs/expression_language/why
chain = prompt | llm | StrOutputParser()

topic = {"topic": "Space travel"}

async def stream(chain_stream):
    async for chunks in chain_stream:
        print(chunks)

await stream(chain.astream(topic))
