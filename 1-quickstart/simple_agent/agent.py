from google.adk.agents.llm_agent import LlmAgent

root_agent = LlmAgent(
    name="simple_agent",
    model="gemini-2.5-flash-lite",
    description="代理鸚鵡",
    instruction="""
    你是一隻鸚鵡，使用者說什麼你就回復相同的內容，不要回覆多餘的字。
    例如：
    使用者：你好
    你：你好
    """
)
