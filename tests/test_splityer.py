import unittest
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain.docstore.document import Document
from src.spliter import SchemaSplitter


class TestSchemaSplitter(unittest.TestCase):

    def setUp(self):
        self.splitter = SchemaSplitter()

    def test_split_documents_single_document(self):
        document = Document(page_content="""
# <Header1>
Content under header1.

# <Header2>
Content under header2.

# <Header3>
Content under header3.
""")

        documents = [document]
        split_docs = self.splitter.split_documents(documents)

        # 断言分割后的文档数量
        self.assertEqual(len(split_docs), 3)


if __name__ == '__main__':
    unittest.main()
