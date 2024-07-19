# coding: utf-8
from typing import List

from langchain.schema import BaseRetriever
from langchain.pydantic_v1 import Field, BaseModel
from langchain.output_parsers import PydanticOutputParser
from langchain.chains import LLMChain
from langchain.retrievers.multi_query import MultiQueryRetriever, LineListOutputParser
from prompt import MULTI_QUERY_PROMPT_TEMPLATE


# Output parser will split the LLM result into a list of queries


def get_multi_query_schema_retiever(retriever: BaseRetriever, model: BaseModel) -> BaseRetriever:
    output_parser = LineListOutputParser()

    llm_chain = LLMChain(llm=model, prompt=MULTI_QUERY_PROMPT_TEMPLATE, output_parser=output_parser)

    retriever = MultiQueryRetriever(
        retriever=retriever, llm_chain=llm_chain, parser_key="lines"
    )

    return retriever
