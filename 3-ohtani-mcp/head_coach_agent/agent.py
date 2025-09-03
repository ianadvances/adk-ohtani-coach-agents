"""

"""

from google.adk.agents import SequentialAgent, ParallelAgent

from .subagents.scout_coach_agent import scout_coach_agent
from .subagents.analytics_coach_agent import analytics_coach_agent
from .subagents.data_coach_agent.agent import data_coach_agent

# --- 1. Create Parallel Agent ---
reference_coach_agent = ParallelAgent(
    name="reference_coach_agent",
    sub_agents=[scout_coach_agent, data_coach_agent]
)

# --- 2. Create Sequential Agent ---
root_agent = SequentialAgent(
    name="head_coach_agent",
    sub_agents=[reference_coach_agent, analytics_coach_agent],
)