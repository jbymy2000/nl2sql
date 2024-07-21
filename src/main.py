from chain import get_chain
from callback import OutCallbackHandler
import asyncio
from util import clear_vectorstore, schema_index, get_record_manager, get_script_directory
from spliter import SchemaSplitter
from loader import SchemaLoader
from util import get_llm
from dotenv import load_dotenv
from langchain import hub
from langchain.memory import ConversationSummaryBufferMemory
from pydantic import BaseModel, Field
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun
from langchain_core.tools import BaseTool, tool
from langchain.agents import AgentExecutor, create_react_agent
import streamlit as st
import os

from config import ZHIPU_API_KEY, OPENAI_API_KEY

# 加载必要的参数
load_dotenv()
serper_api_key = os.getenv("SERPER_API_KEY")
browserless_api_key = os.getenv("BROWSERLESS_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

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


@tool
async def gen_sql(message: str) -> str:
    """generate a sql according query"""
    print("agent hit")
    chain = get_chain(out_callback=None)
    out_callback = OutCallbackHandler()
    task = asyncio.create_task(
        chain.ainvoke({"question": [message]}, config={"callbacks": [out_callback]})
    )

    response = ""
    async for new_token in out_callback.aiter():
        response += new_token
    out_callback.done.clear()

    async for new_token in out_callback.aiter():
        response += new_token

    res = await task
    response += "\n\n" + res["schema_context"] + "\n"

    return response


class RAGSQLTool(BaseTool):
    name = "scrape_website"
    description = "useful when you need to get data from a website url, passing both url and objective to the function; DO NOT make up any url, the url should only be from the search results"

    def __init__(self):
        super().__init__()
        self.name = "rag_sql_tool"
        self.description = (
            "A tool designed to convert natural language questions into SQL queries using RAG (Retrieval-Augmented Generation). "
            "This tool retrieves table information dynamically from the RAG system to construct accurate SQL queries based on your input. "
            "Provide a natural language question, and it will generate the corresponding SQL query. "
            "Example inputs: 'How many users signed up in the last month?', 'What is the average age of users?'. "
            "Example outputs: 'SELECT COUNT(*) FROM users WHERE signup_date >= DATE_SUB(NOW(), INTERVAL 1 MONTH);', "
            "'SELECT AVG(age) FROM users;'."
        )

    async def _run(self, message: str) -> str:
        """
        Convert natural language questions into SQL queries using RAG (Retrieval-Augmented Generation).

        Args:
            message (str): The natural language question to convert into an SQL query.

        Returns:
            str: The generated SQL query.
        """
        return gen_sql(message)

    async def _arun(self, url: str):
        """
        Convert natural language questions into SQL queries using RAG (Retrieval-Augmented Generation).

        Args:
            message (str): The natural language question to convert into an SQL query.

        Returns:
            str: The generated SQL query.
        """
        raise NotImplementedError("error here")


# 创建工具实例
rag_sql_tool = RAGSQLTool()


prompt = hub.pull("hwchase17/react")
#初始化记忆类型
memory = ConversationSummaryBufferMemory(
    memory_key="memory", return_messages=True, llm=get_llm(), max_token_limit=300)

# 使用@tool装饰器定义工具

# 定义输入模式
class MultiplySchema(BaseModel):
    first_int: int = Field(..., description="第一个整数")
    second_int: int = Field(..., description="第二个整数")

# 定义工具
class MultiplyTool(BaseTool):
    name = "multiply"
    description = "对两个整数进行乘法运算"

    args_schema = MultiplySchema

    def _run(self, first_int: int, second_int: int) -> int:
        return first_int * second_int

    async def _arun(self, first_int: int, second_int: int) -> int:
        return first_int * second_int

# 使用工具
multiply_tool = MultiplyTool()

@tool
def magic_function(input: int) -> int:
    """Applies a magic function to an input."""
    return input + 2

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
wikipedia = WikipediaQueryRun(api_wrapper=api_wrapper)
#初始化 agent 可使用的工具集合
tools = [rag_sql_tool, multiply_tool, magic_function,wikipedia]

prompt = hub.pull("hwchase17/react")
chat_model_with_stop = get_llm().bind(stop=["```\n\nObservation:"])
# Choose the LLM to use
agent = create_react_agent(chat_model_with_stop, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools,
    handle_parsing_errors=True,early_stopping_method="force",max_execution_time=6,
    verbose=True)

def main():
    st.set_page_config(page_title="AI Assistant Agent", page_icon=":dolphin:")

    st.header("LangChain SQL GEN -- Agent", divider='rainbow')
    st.header("AI Agent :blue[助理] :dolphin:")

    query = st.text_input("请提问题和需求：")

    if query:
        st.write(f"开始思考 【 {query}】 请稍等")

        # 使用 asyncio.run 来运行异步函数
        result = agent_executor.invoke({"input": query})
        st.info(result)


if __name__ == '__main__':
    init_vectorstore()
    main()
