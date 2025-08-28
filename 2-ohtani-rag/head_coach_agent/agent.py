"""

"""

from google.adk.agents import SequentialAgent, ParallelAgent, LoopAgent

from .subagents.sql_coach_agent import sql_coach_agent
from .subagents.fetching_coach_agent import fetching_coach_agent
from .subagents.retrieval_coach_agent import retrieval_coach_agent
from .subagents.scout_coach_agent import scout_coach_agent
from .subagents.analytics_coach_agent import analytics_coach_agent

# --- 1. Create Loop Agent ---
query_coach_agent = LoopAgent(
    name="query_coach_agent",
    max_iterations=3,
    sub_agents=[sql_coach_agent, fetching_coach_agent],
)

# --- 2. Create Sequential Agent ---
data_coach_agent = SequentialAgent(
    name="data_coach_agent",
    sub_agents=[retrieval_coach_agent, query_coach_agent],
)

# --- 3. Create Parallel Agent ---
reference_coach_agent = ParallelAgent(
    name="reference_coach_agent",
    sub_agents=[scout_coach_agent, data_coach_agent]
)

# --- 4. Create Sequential Agent ---
root_agent = SequentialAgent(
    name="head_coach_agent",
    sub_agents=[reference_coach_agent, analytics_coach_agent],
)
