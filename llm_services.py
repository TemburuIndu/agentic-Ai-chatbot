# llm_services.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from config import RAG_LLM, LLM_STREAMING_ENABLED
from prompt_template import TEMPLATE

# --- Prompt Template ---
prompt = ChatPromptTemplate.from_template(TEMPLATE)

# --- Simple LLM Chain ---
rag_chain = prompt | RAG_LLM | StrOutputParser()

# --- Streaming Wrapper ---
async def stream_rag_chain(inputs: dict):
    """
    Stream output from Gemini LLM.
    """
    formatted_messages = await prompt.ainvoke(inputs)

    if LLM_STREAMING_ENABLED:
        async for chunk in RAG_LLM.astream(formatted_messages):
            yield chunk.content
    else:
        yield await rag_chain.ainvoke(inputs)