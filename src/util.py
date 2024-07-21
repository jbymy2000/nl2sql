from langchain.callbacks.manager import Callbacks
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from langchain.indexes import SQLRecordManager, index
from typing import List, Dict
from collections import defaultdict
from langchain.indexes._api import _batch
from config import ZHIPU_API_KEY,OPENAI_API_KEY
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document


# def get_llm(
#         streaming: bool = True,
#         callbacks: Callbacks = None) -> ChatOpenAI:
#     llm = ChatOpenAI(
#         temperature=0,
#         model="gpt-3.5-turbo",
#         openai_api_key=OPENAI_API_KEY,
#         # openai_api_base="https://open.bigmodel.cn/api/paas/v4/",
#         streaming=streaming,
#         callbacks=callbacks
#     )
#     return llm
#
def get_llm(
        streaming: bool = True,
        callbacks: Callbacks = None) -> ChatOpenAI:
    llm = ChatOpenAI(
        temperature=0,
        model="glm-4-alltools",
        openai_api_key=ZHIPU_API_KEY,
        openai_api_base="https://open.bigmodel.cn/api/paas/v4/",
        streaming=streaming,
        callbacks=callbacks
    )
    return llm

def get_vectorstore(collection_name: str = "schema") -> Chroma:
    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=get_cached_embedder(),
        collection_name=collection_name)

    return vectorstore

def get_cached_embedder() -> CacheBackedEmbeddings:
    fs = LocalFileStore("./embeddings")
    underlying_embeddings = OpenAIEmbeddings()

    cached_embedder = CacheBackedEmbeddings.from_bytes_store(
        underlying_embeddings, fs, namespace=underlying_embeddings.model
    )
    return cached_embedder


def get_record_manager(namespace: str = "schema") -> SQLRecordManager:
    return SQLRecordManager(
        f"chroma/{namespace}", db_url="sqlite:///sql_record_manager_cache.sql"
    )


def clear_vectorstore(collection_name: str = "schema") -> None:
    record_manager = get_record_manager(collection_name)
    vectorstore = get_vectorstore(collection_name)

    index([], record_manager, vectorstore, cleanup="full", source_id_key="source")


def schema_index(docs: List[Document], show_progress: bool = True) -> Dict:
    info = defaultdict(int)

    record_manager = get_record_manager("schema")
    vectorstore = get_vectorstore("schema")

    pbar = None
    if show_progress:
        from tqdm import tqdm
        pbar = tqdm(total=len(docs))

    for docs in _batch(100, docs):
        result = index(
            docs,
            record_manager,
            vectorstore,
            cleanup=None,
            source_id_key="source",
        )
        for k, v in result.items():
            info[k] += v

        if pbar:
            pbar.update(len(docs))

    if pbar:
        pbar.close()

    return dict(info)

import os
import sys
def get_script_path():
    return os.path.abspath(sys.argv[0])
def get_script_directory():
    return os.path.dirname(get_script_path())

def main():
    # 获取带缓存功能的嵌入器
    cached_embedder = get_cached_embedder()

    # 示例文本
    texts = "你好，世界！"

    # 生成嵌入
    embeddings = cached_embedder.embed_query(texts)

    # 打印嵌入向量
    for text, embedding in zip(texts, embeddings):
        print(f"Text: {text}")
        print(f"Embedding: {embedding}\n")