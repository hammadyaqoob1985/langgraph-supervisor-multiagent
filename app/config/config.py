import boto3
from langchain_community.vectorstores import FAISS
from langchain_aws import ChatBedrockConverse, BedrockEmbeddings
import os


bedrock_client = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_DEFAULT_REGION"))
llm = ChatBedrockConverse(
    model="eu.anthropic.claude-3-7-sonnet-20250219-v1:0",
    temperature=0,
    max_tokens=None,
    client=bedrock_client,
    provider="anthropic"
)

embeddings = BedrockEmbeddings(
    client=bedrock_client,
    model_id="amazon.titan-embed-text-v2:0"  # Replace with your desired model
)

def initialize_faiss_db():
    kb_path = os.path.join(os.path.dirname(__file__), 'doctor_information.txt')
    if os.path.exists(kb_path):
        with open(kb_path, 'r', encoding='utf-8') as f:
            documents = [line.strip() for line in f if line.strip()]
        return FAISS.from_texts(documents, embeddings)
    else:
        return None

faiss_db = initialize_faiss_db()
