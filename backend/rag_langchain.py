from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores  import Chroma

embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

def process_pdf(file_path):
    loader=PyPDFLoader(file_path)
    documents=loader.load()
    chunks=text_splitter.split_documents(documents)
    db=Chroma.from_documents(chunks,embeddings,persist_directory="/tmp/chroma_langchain")
    return db

def retrieve(query,db):
    results=db.similarity_search(query,k=3)
    return[doc.page_content for doc in results]