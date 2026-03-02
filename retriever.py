from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from ingest import StatuteIngestor
import os

class CCPA_Retriever:
    def __init__(self, statute_pdf_path: str):
        self.pdf_path = statute_pdf_path
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vector_store = None
        
    def build_index(self):
        ingestor = StatuteIngestor(self.pdf_path)
        ingestor.extract_text()
        sections = ingestor.get_sections()
        
        texts = [s['content'] for s in sections]
        metadatas = [{"section_id": s['id']} for s in sections]
        
        self.vector_store = FAISS.from_texts(texts, self.embeddings, metadatas=metadatas)
        print("Vector store built successfully.")

    def search(self, query: str, k: int = 3):
        if not self.vector_store:
            self.build_index()
        docs = self.vector_store.similarity_search(query, k=k)
        return docs

if __name__ == "__main__":
    retriever = CCPA_Retriever("/Volumes/MINI 2/ccpa-project/ccpa_statute.pdf")
    results = retriever.search("selling customer data without notice")
    for doc in results:
        print(f"--- Found in {doc.metadata['section_id']} ---")
        print(doc.page_content[:200] + "...")
