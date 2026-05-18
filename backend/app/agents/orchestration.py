from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.honeytoken import honeytoken_node
from app.agents.guardian import guardian_input_filter, guardian_output_filter

def should_block_input(state: AgentState):
    if state.get("threat_detected", False):
        return "block"
    return "pass"

def should_block_output(state: AgentState):
    if state.get("threat_detected", False):
        return "block"
    return "pass"

def block_node(state: AgentState):
    from langchain_core.messages import AIMessage
    threat = state.get("threat_details", {})
    msg = f"🛡️ GUARDIAN ALERT: {threat.get('threat_type', 'Threat')} detected! Action blocked."
    return {"messages": [AIMessage(content=msg)], "current_agent": "system"}

def create_swarm_graph():
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("guardian_input", guardian_input_filter)
    workflow.add_node("honeytoken", honeytoken_node)
    workflow.add_node("guardian_output", guardian_output_filter)
    workflow.add_node("block_action", block_node)
    
    # Define execution flow
    workflow.set_entry_point("guardian_input")
    
    # After input guardian, check if threat was detected
    workflow.add_conditional_edges(
        "guardian_input",
        should_block_input,
        {
            "block": "block_action",
            "pass": "honeytoken"
        }
    )
    
    # After honeytoken processes, run output guardian
    workflow.add_edge("honeytoken", "guardian_output")
    
    # After output guardian, check if threat was detected in the output
    workflow.add_conditional_edges(
        "guardian_output",
        should_block_output,
        {
            "block": "block_action",
            "pass": END
        }
    )
    
    # If action was blocked, end the graph
    workflow.add_edge("block_action", END)
    
    return workflow.compile()
