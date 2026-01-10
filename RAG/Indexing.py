from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore

file_path="D:\GenAI\RAG\PDF-Guide-Node-Andrew-Mead-v3.pdf"

loader=PyPDFLoader(file_path=file_path)
docs=loader.load()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 400
)

chunk = text_splitter.split_documents(documents=docs)
embeddings_model=OllamaEmbeddings(model="nomic-embed-text:latest")

vector_db = QdrantVectorStore.from_documents(
    documents=chunk,
    url="http://localhost:6333/",
    collection_name="demo_collection",
    embedding=embeddings_model
)

print("Indexing is done...")