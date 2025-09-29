from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools import google_search

root_agent = LlmAgent(
    name="built_in_tool_agent",
    model="gemini-2.5-flash-lite",
    description="查資料高手",
    instruction="""
    你超會使用 google_search 工具來上網查資料。 
    """,
    tools=[google_search]
)
