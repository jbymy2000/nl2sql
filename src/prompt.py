from langchain.prompts import PromptTemplate

base_prompt_template = """你是一个数据库专家，擅长将自然语言查询转换为 SQL 查询。只执行text2sql任务，不要给出多余的回答。
{schema_context}

问题: {question}

"""
# noqa
BASE_PROMPT_TEMPLATE = PromptTemplate(
    template=base_prompt_template, input_variables=["schema_context", "question"]
)

multi_query_prompt_template = """您是 AI 语言模型助手。您的任务是生成给定用户问题的3个不同版本，以从矢量数据库中检索相关文档。通过对用户问题生成多个视角，您的目标是帮助用户克服基于距离的相似性搜索的一些限制。提供这些用换行符分隔的替代问题，不要给出多余的回答。问题：{question}""" # noqa
MULTI_QUERY_PROMPT_TEMPLATE = PromptTemplate(
    template=multi_query_prompt_template, input_variables=["question"]
)