from langgraph.graph import StateGraph, START, END
from agents import AgentState, ideation_agent, financial_check_agent, arbitrator_agent
from langchain_core.messages import HumanMessage

workflow = StateGraph(AgentState)

workflow.add_node("ideation", ideation_agent)
workflow.add_node("financial_check", financial_check_agent)
workflow.add_node("arbitrator", arbitrator_agent)

workflow.add_edge(START, "ideation")
workflow.add_edge("ideation", "financial_check")
workflow.add_edge("financial_check", "arbitrator")
workflow.add_edge("arbitrator", END)

app = workflow.compile()

if __name__ == "__main__":
    user_vibe = "I have a budget of $1500. I want somewhere with amazing food, a bohemian artistic aesthetic, but not an overcrowded commercial tourist trap."
    print(f"User Request: {user_vibe}\n" + "=" * 50)

    events = app.stream({"messages": [HumanMessage(content=user_vibe)]})
    for event in events:
        for node_name, output in event.items():
            if "messages" in output:
                print(f"\n[{node_name.upper()}]:\n", output["messages"][-1].content)
            elif "compiled_deals" in output:
                print(f"\n[{node_name.upper()}]: Tracking Engine Logs: ", output["compiled_deals"])
