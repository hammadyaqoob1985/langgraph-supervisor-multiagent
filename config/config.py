from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

def initialize_faiss_db():
    kb_path = os.path.join(os.path.dirname(__file__), 'doctor_information.txt')
    if os.path.exists(kb_path):
        with open(kb_path, 'r', encoding='utf-8') as f:
            documents = [line.strip() for line in f if line.strip()]
        return FAISS.from_texts(documents, embeddings)
    else:
        return None

faiss_db = initialize_faiss_db()
