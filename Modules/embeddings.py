from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os
load_dotenv()

api_key=os.getenv("GOOGLE_API_KEY")
# print("API KEY:", api_key)
print("API KEY FOUND:", api_key is not None)

embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=api_key
)
def create_embeddings(chunks):
    embeddings=[]
    for chunk in chunks:
        vector=embedding_model.embed_query(chunk)
        embeddings.append(vector)
    return embeddings
