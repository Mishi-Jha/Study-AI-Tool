import chromadb
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader

model=SentenceTransformer('all-MiniLM-L6-v2')
client=chromadb.PersistentClient(path="./chroma_db")
collection=client.get_or_create_collection(name="notes")

def process_pdf(file_path):
    reader=PdfReader(file_path)
    text=""
    for page in reader.pages:
        text+=page.extract_text()
        
    chunks=[]
    for i in range(0,len(text),500):
        chunks.append(text[i:i+500])

    embeddings=model.encode(chunks)
    collection.add(
        documents=chunks,
        embeddings=embeddings.tolist(),
        ids=[str(i) for i in range(len(chunks))]
    )

def retrieve(query):
    query_embedding=model.encode([query])
    results=collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=3
    )    
    return results['documents'][0]