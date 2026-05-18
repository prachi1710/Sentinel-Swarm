from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.orchestration import create_swarm_graph
from app.services.neo4j_client import neo4j_client
from app.services.redis_client import publish_event
from langchain_core.messages import HumanMessage

router = APIRouter()
swarm_app = create_swarm_graph()

class SimulationRequest(BaseModel):
    user_id: str = "attacker_1"
    payload: str

@router.post("/simulate")
async def simulate_attack(req: SimulationRequest):
    initial_state = {
        "messages": [HumanMessage(content=req.payload)],
        "threat_detected": False,
        "threat_details": {},
        "current_agent": "user"
    }
    
    # Run the langgraph agent workflow
    result_state = swarm_app.invoke(initial_state)
    
    threat_detected = result_state.get("threat_detected", False)
    threat_details = result_state.get("threat_details", {})
    last_message = result_state["messages"][-1].content if result_state["messages"] else ""
    
    # Log interaction to Neo4j Graph
    neo4j_client.log_interaction(
        user_id=req.user_id,
        agent_id="honeytoken_support",
        threat_detected=threat_detected,
        threat_details=threat_details
    )
    
    # Broadcast event to frontend via Redis -> WebSockets
    publish_event("simulation_result", {
        "user_id": req.user_id,
        "threat_detected": threat_detected,
        "threat_details": threat_details,
        "response": last_message
    })
    
    return {
        "status": "success",
        "threat_detected": threat_detected,
        "response": last_message,
        "details": threat_details
    }

@router.get("/graph")
async def get_graph():
    return neo4j_client.get_graph()
