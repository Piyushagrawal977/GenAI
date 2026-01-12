from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from typing import Optional, Literal
import ollama


client = ollama.Client(
    host="http://127.0.0.1:11434"
)

class State(TypedDict):
    user_query:str
    llm_response:Optional [str]

def model1(state:State):
    print("Model1")
    response = client.chat(
        model="qwen2.5:7b",
        messages=[{"role":"user","content":state['user_query']}]
    )
    state["llm_response"]=response.message.content
    return state

def evaluation(state:State):
    if False:
        return "endNode"
    return "model2"

def model2(state:State):
    print("Model2")
    response = client.chat(
        model="qwen2.5:7b",
        messages=[{"role":"user","content":state['user_query']}]
    )
    state["llm_response"]=response.message.content
    return state

def endNode(state:State):
    return state


graph_build = StateGraph(State)
graph_build.add_node('model1',model1),
graph_build.add_node('evaluation',evaluation)
graph_build.add_node('model2',model2)
graph_build.add_node('endNode',endNode)

graph_build.add_edge(START,"model1")
graph_build.add_conditional_edges(
    "model1",
    evaluation,
    {
        "model2": "model2",    # these two lines are optional
        "endNode": "endNode",
    },
)

graph_build.add_edge("model2","endNode")
graph_build.add_edge("endNode",END)

graph=graph_build.compile()
update_graph=graph.invoke(State({"user_query":"what is the sum of 2+2"}))

print(update_graph)