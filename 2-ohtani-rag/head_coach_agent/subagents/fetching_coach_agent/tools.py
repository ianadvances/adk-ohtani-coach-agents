"""

"""

import sqlite3
import pandas as pd
import traceback
import os
from typing import Any, Dict
from google.adk.tools.tool_context import ToolContext


def execute_sql(sql: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    執行 SQL 查詢。

    Args:
        sql: 要執行的 SQL
        tool_context: 工具調用的上下文環境，這裡用來設置狀態

    Returns:
        Dict[str, Any]: 包含以下內容的字典：
            - result: 'failed' 或 'success'
            - data: 查詢結果
    """
    
    try:
        # 獲取數據庫文件路徑
        db_path = os.path.join(os.path.dirname(__file__), "stats.db")
        
        # 檢查數據庫文件是否存在
        if not os.path.exists(db_path):
            error_msg = f"Database file not found: {db_path}"
            tool_context.state["review_feedback"] = error_msg
            return {
                "result": "failed",
                "data": "error",
            }
        
        # 連接到 SQLite 數據庫
        conn = sqlite3.connect(db_path)
        
        # 確保 SQL 中沒有 ``` 符號
        sql = sql.replace("```", "")
        
        # 執行 SQL 查詢並獲取結果
        df = pd.read_sql_query(sql, conn)
        
        # 關閉數據庫連接
        conn.close()
        
        # 將 DataFrame 轉換為 CSV 格式的字符串
        csv_data = df.to_csv(index=False)
        
        return {
            "result": "success",
            "data": csv_data,
        }
        
    except Exception as e:
        # 獲取完整的錯誤信息
        error_log = traceback.format_exc()
        
        # 將錯誤信息存儲到 tool_context.state
        tool_context.state["review_feedback"] = error_log
        
        return {
            "result": "failed",
            "data": "error",
        }


def exit_loop(query_result: Dict[str, Any], tool_context: ToolContext) -> Dict[str, Any]:
    """
    確認成功執行 SQL 查詢並且已取得使用者所需資料，將結果存儲並結束循環。

    Args:
        query_result: execute_sql 工具的返回結果
        tool_context: 工具調用的上下文環境，這裡用來設置狀態

    Returns:
        空字典
    """
    
    # 將 SQL 查詢結果存儲到 state 中，供後續 agent 使用
    tool_context.state["query_data"] = query_result
    
    # 設置 escalate 來結束循環
    tool_context.actions.escalate = True
    return {}