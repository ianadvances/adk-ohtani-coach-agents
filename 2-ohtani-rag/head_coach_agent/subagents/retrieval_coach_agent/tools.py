"""

"""

import os
from typing import Any, Dict
from google.adk.tools.tool_context import ToolContext
import chromadb
from google import genai
from google.genai import types
from chromadb import Documents, EmbeddingFunction, Embeddings

client = genai.Client()

class GeminiEmbeddingFunction(EmbeddingFunction):
    """自定義的 Gemini 嵌入函數類"""
    
    def __call__(self, input: Documents) -> Embeddings:
        """將文檔列表轉換為嵌入向量列表"""
        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=input,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_QUERY"
            )
        )
        return response.embeddings[0].values

def retrieve_schema_and_example(text: str) -> Dict[str, Any]:
    """
    根據使用者的問題，使用 RAG 方式提供相關的 schema 及範例。

    Args:
        text: 使用者的問題，將此進行 embedding 並檢索相關的 schema 及範例

    Returns:
        Dict[str, Any]: 包含以下內容的字典：
            - result: 'failed' 或 'success'
            - schema: schema 內容及說明
            - examples: sql 範例
    """
    try:
        # 初始化 ChromaDB 客戶端
        schema_client = chromadb.PersistentClient(path=os.path.join(os.path.dirname(__file__), "vdb_schema"))
        examples_client = chromadb.PersistentClient(path=os.path.join(os.path.dirname(__file__), "vdb_examples"))
        
        # 獲取集合
        schema_collection = schema_client.get_or_create_collection(
            name="database_schema",
            embedding_function=GeminiEmbeddingFunction()
        )
        
        examples_collection = examples_client.get_or_create_collection(
            name="query_examples",
            embedding_function=GeminiEmbeddingFunction()
        )
        
        # 檢索相關的 schema
        schema_results = schema_collection.query(
            query_texts = [text],
            n_results = 2
        )
        
        # 檢索相關的範例
        examples_results = examples_collection.query(
            query_texts = [text],
            n_results = 2 
        )
        
        # 提取檢索結果
        schema_list = schema_results['documents'][0]
        schema_content = "\n\n".join(schema_list)
        
        examples_list = examples_results['documents'][0]
        examples_content = "\n\n".join(examples_list)

        
        return {
            "result": "success",
            "schema": schema_content,
            "examples": examples_content,
        }
        
    except Exception as e:
        print(f"RAG 檢索失敗: {e}")
        # 如果 RAG 檢索失敗，返回失敗
        return {
            "result": "failed",
            "schema": "",
            "examples": "",
        }
