import asyncio
import json
import logging
import os
import sqlite3

import mcp.server.stdio  # 用於作為 stdio 伺服器運行
from dotenv import load_dotenv

from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type

from mcp import types as mcp_types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions

load_dotenv()

# --- 日誌設定 ---
LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), "mcp_server_activity.log")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE_PATH, mode="w", encoding="utf-8"),
    ],
)
# --- 日誌設定結束 ---

# 指向本地的 stats.db
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "stats.db")


# --- 資料庫工具函數 ---
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # 以欄位名稱存取欄位
    return conn


def list_db_tables(dummy_param: str) -> dict:
    """列出 SQLite 資料庫中的所有表格。

    Args:
        dummy_param (str): 此參數不被函數使用，
                           但有助於確保架構生成。預期為非空字串。
    Returns:
        dict: 包含 'success' (bool)、'message' (str) 和
              'tables' (list[str]) 鍵的字典，成功時包含表格名稱。
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return {
            "success": True,
            "message": "表格列出成功。",
            "tables": tables,
        }
    except sqlite3.Error as e:
        return {"success": False, "message": f"列出表格時發生錯誤：{e}", "tables": []}
    except Exception as e:
        return {
            "success": False,
            "message": f"列出表格時發生意外錯誤：{e}",
            "tables": [],
        }


def get_table_schema(table_name: str) -> dict:
    """取得特定表格的架構（欄位名稱和類型）。"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info('{table_name}');")  # 使用 PRAGMA 取得架構
    schema_info = cursor.fetchall()
    conn.close()
    if not schema_info:
        raise ValueError(f"找不到表格 '{table_name}' 或無架構資訊。")

    columns = [{"name": row["name"], "type": row["type"]} for row in schema_info]
    return {"table_name": table_name, "columns": columns}


def query_db_table(table_name: str, columns: str, condition: str) -> list[dict]:
    """使用可選條件查詢表格。

    Args:
        table_name: 要查詢的表格名稱。
        columns: 要檢索的欄位清單，以逗號分隔（例如 "id, score"）。預設為 "*"。
        condition: 可選的 SQL WHERE 子句條件（例如 "id = 1" 或 "recent_game_rank = 1"）。
    Returns:
        字典清單，每個字典代表一行資料。
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    query = f"SELECT {columns} FROM {table_name}"
    if condition:
        query += f" WHERE {condition}"
    query += ";"

    try:
        cursor.execute(query)
        results = [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        conn.close()
        raise ValueError(f"查詢表格 '{table_name}' 時發生錯誤：{e}")
    conn.close()
    return results


def execute_sql_query(sql_query: str) -> list[dict]:
    """執行自定義 SQL 查詢。

    Args:
        sql_query: 要執行的 SQL 查詢語句。
    Returns:
        字典清單，每個字典代表一行資料。
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(sql_query)
        results = [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        conn.close()
        raise ValueError(f"執行 SQL 查詢時發生錯誤：{e}")
    conn.close()
    return results


# --- MCP 伺服器設定 ---
logging.info(
    "正在為 SQLite 資料庫建立 MCP 伺服器實例..."
)
app = Server("sqlite-mcp-server")

# 將資料庫工具函數包裝為 ADK FunctionTools
ADK_DB_TOOLS = {
    "list_db_tables": FunctionTool(func=list_db_tables),
    "get_table_schema": FunctionTool(func=get_table_schema),
    "query_db_table": FunctionTool(func=query_db_table),
    "execute_sql_query": FunctionTool(func=execute_sql_query),
}


@app.list_tools()
async def list_mcp_tools() -> list[mcp_types.Tool]:
    """列出此伺服器公開工具的 MCP 處理程序。"""
    logging.info(
        "MCP 伺服器：收到 list_tools 請求。"
    )
    mcp_tools_list = []
    for tool_name, adk_tool_instance in ADK_DB_TOOLS.items():
        if not adk_tool_instance.name:
            adk_tool_instance.name = tool_name

        mcp_tool_schema = adk_to_mcp_tool_type(adk_tool_instance)
        logging.info(
            f"MCP 伺服器：工具：{mcp_tool_schema.name}，輸入架構：{mcp_tool_schema.inputSchema}"
        )
        mcp_tools_list.append(mcp_tool_schema)
    return mcp_tools_list


@app.call_tool()
async def call_mcp_tool(name: str, arguments: dict) -> list[mcp_types.TextContent]:
    """執行 MCP 客戶端請求的工具呼叫的 MCP 處理程序。"""
    logging.info(
        f"MCP 伺服器：收到對 '{name}' 的 call_tool 請求，參數：{arguments}"
    ) 

    if name in ADK_DB_TOOLS:
        adk_tool_instance = ADK_DB_TOOLS[name]
        try:
            adk_tool_response = await adk_tool_instance.run_async(
                args=arguments,
                tool_context=None,  # type: ignore
            )
            logging.info(  
                f"MCP 伺服器：ADK 工具 '{name}' 已執行。回應：{adk_tool_response}"
            )
            response_text = json.dumps(adk_tool_response, indent=2)
            return [mcp_types.TextContent(type="text", text=response_text)]

        except Exception as e:
            logging.error(
                f"MCP 伺服器：執行 ADK 工具 '{name}' 時發生錯誤：{e}", exc_info=True
            )
            error_payload = {
                "success": False,
                "message": f"執行工具 '{name}' 失敗：{str(e)}",
            }
            error_text = json.dumps(error_payload)
            return [mcp_types.TextContent(type="text", text=error_text)]
    else:
        logging.warning(
            f"MCP 伺服器：此伺服器找不到/未公開工具 '{name}'。"
        )
        error_payload = {
            "success": False,
            "message": f"此伺服器未實作工具 '{name}'。",
        }
        error_text = json.dumps(error_payload)
        return [mcp_types.TextContent(type="text", text=error_text)]


# --- MCP 伺服器執行器 ---
async def run_mcp_stdio_server():
    """執行 MCP 伺服器，監聽標準輸入/輸出的連接。"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logging.info(
            "MCP Stdio 伺服器：開始與客戶端握手..."
        ) 
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=app.name,
                server_version="0.1.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
        logging.info(
            "MCP Stdio 伺服器：執行迴圈結束或客戶端已斷線。"
        ) 


if __name__ == "__main__":
    logging.info(
        "Launching SQLite DB MCP Server via stdio..."
    ) 
    try:
        asyncio.run(run_mcp_stdio_server())
    except KeyboardInterrupt:
        logging.info(
            "\nMCP Server (stdio) stopped by user."
        ) 
    except Exception as e:
        logging.critical(
            f"MCP Server (stdio) encountered an unhandled error: {e}", exc_info=True
        )
    finally:
        logging.info(
            "MCP Server (stdio) process exiting."
        )