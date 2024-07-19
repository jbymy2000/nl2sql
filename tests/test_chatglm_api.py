import unittest
import sys
from src.util import get_llm
sys.path.append('/home/rex/Documents/Codes/ai_girlfriend/src')
print(sys.path)




class TestModelInitialization(unittest.TestCase):

    def test_llm(self):
        get_llm()
    def test_initialize_model_and_tokenizer(self):
        import os
        from langchain_openai import ChatOpenAI
        from langchain.prompts import (
            ChatPromptTemplate,
            MessagesPlaceholder,
            SystemMessagePromptTemplate,
            HumanMessagePromptTemplate,
        )
        from langchain.chains import LLMChain
        from langchain.memory import ConversationBufferMemory

        llm = ChatOpenAI(
            temperature=0.95,
            model="glm-4",
            openai_api_key="",
            openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
        )
        prompt = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template(
                    "You are a nice chatbot having a conversation with a human."
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{question}")
            ]
        )

        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        conversation = LLMChain(
            llm=llm,
            prompt=prompt,
            verbose=True,
            memory=memory
        )
        print(conversation.invoke({"question": "tell me a joke"}))

if __name__ == '__main__':
    unittest.main()