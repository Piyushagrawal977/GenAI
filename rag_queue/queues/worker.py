from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaEmbeddings
import ollama

embeddings_model=OllamaEmbeddings (model="nomic-embed-text:latest")
vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333/",
    collection_name="demo_collection",
    embedding=embeddings_model
)  

def processor(query:str):
     
    print("Searching on the vectordb")
    search_results = vector_db.similarity_search(query)
    context = "n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])
    system_prompt= f"""
    You are a helpfull AI Assistant who answeres user query based on the available context retrived from a Pdf file along with page_contents and page number. 

    You should only ans the user based on the following context and navigate the user to open the right page number to know more.

    context: {context}

    """
    client = ollama.Client(
        host="http://127.0.0.1:11434"
    )
    response = client.chat(
        model="qwen2.5:7b",
        messages=[
            { 
        "role": "system",
        "content":system_prompt
        },
        {
            "role":"user",
            "content":query
        }
        ]
    )

    print("response is generated")
    return response.message.content

