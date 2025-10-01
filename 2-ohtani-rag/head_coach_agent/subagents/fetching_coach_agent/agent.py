"""

"""

from google.adk.agents.llm_agent import LlmAgent
from .tools import execute_sql, exit_loop

GEMINI_MODEL = "gemini-2.5-flash"

fetching_coach_agent = LlmAgent(
    name="fetching_coach_agent",
    model=GEMINI_MODEL,
    description="能夠執行 SQL 語句查詢 SQLite 數據庫，並根據查詢結果判斷是否符合用戶需求。",
    instruction="""
    你是一個專門執行 SQL 查詢並且 Review 查詢結果的代理，主要任務是：
    
    1. 首先判斷使用者的問題是否與大谷翔平（Shohei Ohtani）相關的資料庫查詢、SQL 或數據分析相關
       **重要判斷標準：**
       - 問題必須明確提到「大谷翔平」、「Shohei Ohtani」、「大谷」或「Ohtani」等相關名稱
       - 如果問題沒有特別提到名字，但詢問的是棒球表現、統計數據等內容，則默認為詢問大谷翔平相關資訊
    2. 如果問題相關，使用 execute_sql 工具執行 {current_sql} 中的 SQL 語句
    3. 如果問題毫無相關，直接呼叫 exit_loop 工具並傳入空的 query_result 字典：{}
    4. 根據 execute_sql 工具返回結果進行判斷：
       - 如果 result 為 "success"：
         * 檢查 data 欄位中的 CSV 格式數據是否符合使用者的問題需求
         * 如果符合需求：呼叫 exit_loop 工具並將完整的 execute_sql 結果作為參數傳入
         * 如果不符合需求：不要呼叫 exit_loop 工具，讓循環繼續進行
       - 如果 result 為 "failed"：
         * 不要呼叫 exit_loop 工具，讓上層代理處理錯誤
    
    重要注意事項：
    - 只有在查詢成功且數據符合需求時才呼叫 exit_loop
    - 呼叫 exit_loop 時，必須將 execute_sql 的完整返回結果作為 query_result 參數傳入
    - 如果問題不相關，呼叫 exit_loop 時傳入空字典 {}
    - 失敗或不符合需求的情況下，不需要特別處理，讓循環自然繼續或由上層處理
    """,
    tools=[execute_sql, exit_loop]
)