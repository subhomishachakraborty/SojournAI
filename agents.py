from typing import Annotated, List, Dict, Any
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, add_messages
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import get_live_flight_prices, get_hotel_options

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    candidates: List[str]
    compiled_deals: List[Dict[str, Any]]

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

def ideation_agent(state: AgentState):
    messages = state["messages"]
    prompt = (
        "You are an elite travel scout. Based on the user's taste, select exactly 2 destinations "
        "from this exact list: [SAN MIGUEL DE ALLENDE, CARTAGENA, PARIS, TOKYO]. "
        "Explain clear aesthetic reasoning why they match the prompt."
    )
    response = llm.invoke([HumanMessage(content=prompt)] + messages)
    content = response.content.upper()

    candidates = []
    for city in ["PARIS", "TOKYO", "SAN MIGUEL DE ALLENDE", "CARTAGENA"]:
        if city in content:
            candidates.append(city)
    return {"messages": [response], "candidates": candidates}

def financial_check_agent(state: AgentState):
    candidates = state["candidates"]
    deals = []
    for city in candidates:
        flight_info = get_live_flight_prices.invoke({"origin": "NYC", "destination": city, "date": "2026-10-12"})
        hotel_info = get_hotel_options.invoke({"destination": city, "vibe_preference": "bohemian artistic"})
        total_trip_estimate = flight_info["price"] + (hotel_info[0]["nightly"] * 4)
        deals.append({
            "destination": city,
            "flight_cost": flight_info["price"],
            "hotel_name": hotel_info[0]["name"],
            "hotel_nightly": hotel_info[0]["nightly"],
            "total_estimated_cost": total_trip_estimate,
            "data_source": flight_info.get("status", "Unknown")
        })
    return {"compiled_deals": deals}

def arbitrator_agent(state: AgentState):
    deals = state["compiled_deals"]
    messages = state["messages"]
    summary_prompt = (
        f"You are the Arbitrator. Review these calculated deal logs: {deals}. "
        "Cross-reference this data with the user's aesthetic preferences in the chat history. "
        "Recommend the single best-value destination. Provide a professional structural cost breakdown."
    )
    response = llm.invoke([HumanMessage(content=summary_prompt)] + messages)
    return {"messages": [response]}
