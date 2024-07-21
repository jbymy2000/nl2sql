from chain import get_chain
from callback import OutCallbackHandler
import gradio as gr
import asyncio
from util import clear_vectorstore, schema_index, get_record_manager, get_script_directory
from spliter import SchemaSplitter
from loader import SchemaLoader
from pprint import pprint
import os
from config import ZHIPU_API_KEY,OPENAI_API_KEY

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def init_vectorstore() -> None:
    record_manager = get_record_manager("schema")
    record_manager.create_schema()
    clear_vectorstore("schema")

    text_splitter = SchemaSplitter.from_tiktoken_encoder(
        chunk_size=100, chunk_overlap=20
    )
    print(f"{get_script_directory()}/schema")
    docs = SchemaLoader(f"{get_script_directory()}/schema").load_and_split(text_splitter=text_splitter)
    info = schema_index(docs)
    print(info)


def run_web():
    chain = get_chain(out_callback=None)

    async def chat(message, history):
        out_callback = OutCallbackHandler()
        task = asyncio.create_task(
            chain.ainvoke({"question": [message]}, config={"callbacks": [out_callback]}))
        async for new_token in out_callback.aiter():
            pass

        out_callback.done.clear()

        response = ""
        async for new_token in out_callback.aiter():
            response += new_token
            yield response

        res = await task
        for new_token in ["\n\n", res["schema_context"], "\n"]:
            response += new_token
            yield response

    demo = gr.ChatInterface(
        fn=chat, examples=["公司有多少人？","sony公司的成立日期"], title="SQL小助手")

    demo.queue()
    demo.launch(share=True)


if __name__ == '__main__':
    init_vectorstore()
    run_web()
