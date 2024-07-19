import unittest
from transformers import AutoModelForCausalLM, AutoTokenizer
import sys
sys.path.append('/home/rex/Documents/Codes/ai_girlfriend/src')
print(sys.path)
from src.models.model import initialize_model_and_tokenizer  # Corrected to use the right import statement




class TestModelInitialization(unittest.TestCase):

    def test_initialize_model_and_tokenizer(self):
        model_name = "shenzhi-wang/Llama3-8B-Chinese-Chat"
        model, tokenizer = initialize_model_and_tokenizer(model_name)

        # 测试模型是否成功加载
        self.assertIsNotNone(model, "模型加载失败")

        # 测试分词器是否成功加载
        self.assertIsNotNone(tokenizer, "分词器加载失败")

if __name__ == '__main__':
    unittest.main()