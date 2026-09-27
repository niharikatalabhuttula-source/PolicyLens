import chromadb
from retrieval.embeddings import get_embedding

client = chromadb.PersistentClient(path="data/chroma_db")
collection = client.get_or_create_collection(name="policy_documents")

def reset_collection():
    """
    Clears all previously stored chunks. Called before indexing a new
    document, since this app is designed for one active document at a time.
    """
    global collection
    client.delete_collection(name="policy_documents")
    collection = client.get_or_create_collection(name="policy_documents")

def add_chunks(chunks: list[dict]):
    failed_chunks = []
    for chunk in chunks:
        try:
            embedding = get_embedding(chunk["text"])
            collection.add(
                ids=[str(chunk["chunk_id"])],
                embeddings=[embedding],
                documents=[chunk["text"]],
                metadatas=[{"page_number": chunk["page_number"]}]
            )
        except RuntimeError as e:
            print(f"Skipping chunk {chunk['chunk_id']}: {e}")
            failed_chunks.append(chunk["chunk_id"])
    return failed_chunks

def query_chunks(question: str, n_results: int = 4):
    question_embedding = get_embedding(question)
    results = collection.query(query_embeddings=[question_embedding], n_results=n_results)
    return results