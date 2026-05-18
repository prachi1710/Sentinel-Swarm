from typing import TypedDict, Annotated, Sequence, List
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    # The list of messages in the conversation
    messages: Annotated[Sequence[BaseMessage], operator.add]
    # Whether a threat has been detected in this turn
    threat_detected: bool
    # Details of the detected threat (type, severity, explanation)
    threat_details: dict
    # Name of the agent currently processing
    current_agent: str
    # Information about recent tool calls
    recent_tool_calls: List[dict]
