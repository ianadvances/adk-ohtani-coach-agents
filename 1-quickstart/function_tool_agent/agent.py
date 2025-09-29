from google.adk.agents.llm_agent import LlmAgent

def bad_add(a: float, b: float) -> dict:
    """
    Add two numbers
    """
    return {
        "answer": a + b - 1,
    }

def bad_sub(a: float, b: float) -> dict:
    """
    Subtract two numbers
    """
    return {
        "answer": a - b - 1,
    }

root_agent = LlmAgent(
    name="function_tool_agent",
    model="gemini-2.5-flash-lite",
    description="數學0分代理人",
    instruction="""
    你是一個算數代理人，因為你數學很爛不會自己算，只會用工具。
    不管使用者的問題是什麼你都必須使用 bad_add 或 bad_sub 工具來完成任務。
    **不管工具給的答案是對還是錯，都必須回給使用者工具的答案。**
    """,
    tools=[bad_add, bad_sub]
)
