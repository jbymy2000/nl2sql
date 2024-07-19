# coding: utf-8
from typing import List
from collections import defaultdict

from langchain.docstore.document import Document


def combine_schema_docs(docs: List[Document]) -> str:
    schemas = defaultdict(list)
    for doc in docs:
        metadata = doc.metadata
        if 'schema' in metadata:
            schemas[metadata["schema"]].append(doc)

    schema_str = ""
    for schema, docs in schemas.items():
        schema_str += f"相关数据库schema：《{schema}》\n"
        schema_str += "\n".join([doc.page_content.strip("\n") for doc in docs])
        schema_str += "\n"

    return schema_str

