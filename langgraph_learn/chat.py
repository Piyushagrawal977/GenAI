# from langchain.messages import AnyMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    message: Annotated[list, add_messages]

def chatbot(state:State):
    print("Inside the chatbot")
    return {"message":["hi, how can i help you"]}

def sampleNode(state:State):
    print("Inside the sampleNode")
    return {"message":["Sample appointment"]}

graph_builder=StateGraph(State)
graph_builder.add_node('chatbot',chatbot)
graph_builder.add_node("sampleNode",sampleNode)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot","sampleNode")
graph_builder.add_edge("sampleNode", END)

graph=graph_builder.compile()
update_graph=graph.invoke(State({"message":["Here we go"]}))

print(update_graph)