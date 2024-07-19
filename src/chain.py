from util import get_llm,get_vectorstore
from langchain.chains.base import Chain
from langchain.schema.runnable import RunnableMap
from langchain.schema.output_parser import StrOutputParser
from prompt import BASE_PROMPT_TEMPLATE
from operator import itemgetter
from langchain.callbacks import AsyncIteratorCallbackHandler
from retriever import get_multi_query_schema_retiever
from combine import combine_schema_docs
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_chain(out_callback: AsyncIteratorCallbackHandler) -> Chain:
    schema_vs = get_vectorstore("schema")

    vs_retriever = schema_vs.as_retriever(search_kwargs={"k": 1})
    multi_query_retriver = get_multi_query_schema_retiever(vs_retriever, get_llm())

    callbacks = [out_callback] if out_callback else []

    chain = (
        RunnableMap(
            {
                "schema_docs": itemgetter("question") | multi_query_retriver,
                "question": lambda x: x["question"]}
        )
        | RunnableMap({
                "schema_docs": lambda x: x["schema_docs"],
                "schema_context": lambda x: combine_schema_docs(x["schema_docs"]),
                "question": lambda x: x["question"],
            }
        )
        | RunnableMap({
                          "schema_docs": lambda x: x["schema_docs"],
                          "schema_context": lambda x: x["schema_context"],
                          "prompt": BASE_PROMPT_TEMPLATE
                      }
        )
        | RunnableMap({
            "schema_context": lambda x: x["schema_context"],
            "answer": itemgetter("prompt") | get_llm(callbacks=callbacks) | StrOutputParser()
        })
    )

    return chain